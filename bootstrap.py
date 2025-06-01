"""Code to bootstrap environment.

*ONLY* use Python Standard Libraries.
"""
import copy
import functools
import logging
import os
import os.path
import pathlib
import subprocess
import sys
import threading
import tomllib
import urllib.parse
import urllib.request
import venv

# Shared variables
VENV_PATH = pathlib.Path('venv')
BIN_PATH = VENV_PATH / 'bin'
DISABLE_VIRTUALENV_ENV_VAR = 'DISABLE_VIRTUALENV'
CORE_PACKAGES = ['pip', 'setuptools']


def bootstrap_config():
    """Grab the config items from pyproject.toml."""
    filename = 'pyproject.toml'
    with open(filename, 'rb') as fp:
        raw = tomllib.load(fp)
    config = raw.get('tool', {}).get('bootstrap', {})
    return config


def filter_setuptools_tgz(filename):
    if filename.startswith('setuptools-') and filename.endswith('.tar.gz'):
        return True
    return False


def create_logger(cls):
    logger_name = cls.__class__.__name__
    return logging.getLogger(logger_name)


class VenvBuilder(venv.EnvBuilder):
    """Subclassing EnvBuilder.

    Docs: https://docs.python.org/3/library/venv.html#api
    """
    my_config_keys = ['additional_packages', 'verbose', 'minimum_python_version']

    def __init__(self):
        self.logger = create_logger(self)
        self.config = bootstrap_config()
        self.logger.debug('Config: %s', self.config)
        super_args = []
        super_kwargs = copy.deepcopy(self.config)
        # Remove config flags not meant for the parent.
        for cur in self.my_config_keys:
            if cur in super_kwargs:
                del super_kwargs[cur]
        super().__init__(*super_args, **super_kwargs)
        self.progress = None
        self.venv_path = VENV_PATH
        self.bin_path = self.venv_path / 'bin'
        self.pip_command = str(self.bin_path / 'pip')
        self.python_command = str(self.bin_path / 'python3')

    @functools.cached_property
    def verbose(self):
        return self.config.get('verbose', False)

    @functools.cached_property
    def additional_packages(self):
        return self.config.get('additional_packages', [])

    @functools.cached_property
    def minimum_python_version(self):
        raw = self.config.get('minimum_python_version', None)
        self.logger.debug('Minimum python version: "%s"', raw)
        if raw is None:
            return ()
        version = tuple(int(i) for i in raw.split('.'))
        self.logger.debug('Converted version: %s', version)
        return version

    def does_venv_exist(self):
        return self.venv_path.exists()

    def _verify_python_version(self):
        raw_version = sys.version_info
        actual_version = (raw_version.major, raw_version.minor)
        self.logger.debug('Actual version: %s', actual_version)
        both = f'actual={actual_version}  wanted={self.minimum_python_version}'
        if actual_version < self.minimum_python_version:
            self.logger.error('Python version too old: %s', both)
            raise SystemExit(11)
        self.logger.debug('Python version ok: %s', both)

    def _disable_create_virtualenv(self):
        if DISABLE_VIRTUALENV_ENV_VAR in os.environ:
            self.logger.info('Disabling venv create')
            return True
        self.logger.debug('Enable venv create')
        return False

    def reader(self, stream, context):
        """
        Read lines from a subprocess' output stream and either pass to a progress
        callable (if specified) or write progress information to sys.stderr.
        """
        progress = self.progress
        while True:
            s = stream.readline()
            if not s:
                break
            if progress is not None:
                progress(s, context)
            else:
                if not self.verbose:
                    sys.stderr.write('.')
                else:
                    sys.stderr.write(s.decode('utf-8'))
                sys.stderr.flush()
        stream.close()

    def install_script(self, context, name, url):
        """Install stuff..."""
        _, _, path, _, _, _ = urllib.parse.urlparse(url)
        fn = os.path.split(path)[-1]
        binpath = context.bin_path
        distpath = os.path.join(binpath, fn)
        # Download script into the virtual environment's binaries folder
        urllib.request.urlretrieve(url, distpath)
        self.logger.debug('Saving file: %s - %s', url, distpath)
        progress = self.progress
        if self.verbose:
            term = '\n'
        else:
            term = ''
        if progress is not None:
            progress(f'Installing {name} ...{term}', 'main')
        else:
            sys.stderr.write(f'Installing {name} ...{term}')
            sys.stderr.flush()
        # Install in the virtual environment
        args = [context.env_exe, fn]
        p = subprocess.Popen(  # pylint: disable=R1732
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=binpath)
        t1 = threading.Thread(target=self.reader, args=(p.stdout, 'stdout'))
        t1.start()
        t2 = threading.Thread(target=self.reader, args=(p.stderr, 'stderr'))
        t2.start()
        p.wait()
        t1.join()
        t2.join()
        if progress is not None:
            progress('done.', 'main')
        else:
            sys.stderr.write('done.\n')
        # Clean up - no longer needed
        os.unlink(distpath)

    def install_setuptools(self, context):
        """
        Install setuptools in the virtual environment.

        :param context: The information for the virtual environment
                        creation request being processed.
        """
        url = 'https://bootstrap.pypa.io/ez_setup.py'
        self.install_script(context, 'setuptools', url)
        # clear up the setuptools archive which gets downloaded
        files = filter(filter_setuptools_tgz, os.listdir(context.bin_path))
        for f in files:
            f = os.path.join(context.bin_path, f)
            self.logger.debug('Removing file: %s', f)
            os.unlink(f)

    def install_pip(self, context):
        """
        Install pip in the virtual environment.

        :param context: The information for the virtual environment
                        creation request being processed.
        """
        url = 'https://bootstrap.pypa.io/get-pip.py'
        self.install_script(context, 'pip', url)

    def _install_package_with_pip(self, package_name, upgrade=True):
        self.logger.debug(
            'Installing package with pip: %s (upgrade=%s)', package_name, upgrade)
        command = [self.pip_command]
        command.append('install')
        if upgrade:
            command.append('--upgrade')
        command.append(package_name)
        self.logger.debug('Running command: %s', command)
        subprocess.check_call(command)
        # TODO check stdout/stderr of command

    def post_setup(self, context):
        self.logger.debug('Post setup')
        if self.with_pip is not None and self.with_pip is True:
            self.logger.debug('Installing packages with pip.')
            for pkg_name in CORE_PACKAGES:
                self._install_package_with_pip(pkg_name)
        else:
            self.logger.debug('Installing core packages directly.')
            self.install_setuptools(context)
            self.install_pip(context)

    def _install_additional_packages(self):
        self.logger.debug('Installing additional packages')
        for pkg_name in self.additional_packages:
            self.logger.debug('Installing package: %s', pkg_name)
            subprocess.check_call([self.pip_command, 'install', pkg_name])

    def __call__(self):
        self.logger.debug('Inside call')
        self._verify_python_version()
        if not self._disable_create_virtualenv():
            self.logger.debug('Creating virtualenv: %s', VENV_PATH)
            self.create(self.venv_path)
        self._install_additional_packages()


class BootstrapCli:  # pylint: disable=R0903
    """Main CLI class."""
    logger_level = 'warning'

    def __init__(self):
        self._init_root_logger()
        self.logger = create_logger(self)

    def _init_root_logger(self):
        # TODO add option to set log level in pyproject.toml
        logger_level = os.environ.get('LOG_LEVEL', self.logger_level)
        logging.basicConfig(level=self.logger_level.upper())
        self.root_logger = logging.getLogger('')
        self.root_logger.setLevel(logger_level.upper())

    def __call__(self):
        self.logger.debug('Inside call')
        builder = VenvBuilder()
        if builder.does_venv_exist():
            self.logger.warning('Path exists: %s', VENV_PATH)
            self.logger.warning('Exiting')
            return
        builder()


if __name__ == '__main__':
    BootstrapCli()()
