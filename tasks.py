"""Actions needed to manage the package itself."""

import logging
import os
import sys

import invoke

import bootstrap

_REQUIREMENTS_FILES_CORE = [
    'requirements.txt',
    'tests/requirements.txt',
]
_REQUIREMENTS_FILES_DEV = ['dev_requirements.txt']
# logging config
_LOGGER_NAME = ''
_LOGGER_LEVEL = 'debug'
logging.basicConfig(level=_LOGGER_LEVEL.upper())
for _cur_logger in ['invoke']:
    logging.getLogger(_cur_logger).setLevel('warning'.upper())
logger = logging.getLogger(_LOGGER_NAME)
#
_BIN_DIR = 'venv/bin'
_PYTHON_PATHS = ['bootstrap.py', 'tasks.py', 'tests', 'src']
_KNOWN_COMMANDS = ['python', 'pip', 'pur', 'pylint', 'isort', 'flake8', 'pytest', ]


def _is_virtual_env_disabled():
    raw = os.environ.get('DISABLE_VIRTUAL_ENV', False)
    return raw is True or raw == 'true'


def _want_dev_installed():
    raw = os.environ.get('DISABLE_DEV_REQUIREMENTS', False)
    return raw is False or raw == 'false'


def _build_command(command):
    if command not in _KNOWN_COMMANDS:
        logger.fatal('Unknown command: %s', command)
        raise SystemExit(11)
    if _is_virtual_env_disabled():
        return command
    return f'{_BIN_DIR}/{command}'


@invoke.task
def info(context):  # pylint: disable=unused-argument
    """Show some info about this package."""
    version = sys.version
    print(f'Python version: {version}')
    print(f'Virtual env disabled: {_is_virtual_env_disabled()}')
    #
    config = bootstrap.bootstrap_config()
    print('Config:')
    for cur_key, cur_value in config.items():
        print(f'  - {cur_key}: {cur_value}')
    #
    print('Commands:')
    for cur in _KNOWN_COMMANDS:
        print(f'  - {_build_command(cur)}')


def _install_requirements_files(filenames):
    pip_cmd = _build_command('pip')
    for cur in filenames:
        cur_cmd = f'{pip_cmd} install -r {cur}'
        logger.debug('Running: %s', cur_cmd)
        invoke.run(cur_cmd)


def _install_this():
    pip_cmd = _build_command('pip')
    cur_cmd = f'{pip_cmd} install -e .'
    logger.debug('Running: %s', cur_cmd)
    invoke.run(cur_cmd)


@invoke.task
def install(context):  # pylint: disable=unused-argument
    """Install all requirements and the "local package" using pip."""
    _install_requirements_files(_REQUIREMENTS_FILES_CORE)
    if _want_dev_installed() is True:
        logger.debug('Installing dev requirements')
        _install_requirements_files(_REQUIREMENTS_FILES_DEV)
    _install_this()


@invoke.task
def update_reqs(context):  # pylint: disable=unused-argument
    """Update any packages in the various requirements files using `pur`."""
    pur_cmd = _build_command('pur')
    pur_args = '--force --requirement'
    req_files = _REQUIREMENTS_FILES_CORE
    req_files.extend(_REQUIREMENTS_FILES_DEV)
    for cur in req_files:
        logger.debug('Updating requirements file: %s', cur)
        invoke.run(f'{pur_cmd} {pur_args} {cur}')


def _check_pip_outdated():
    """Check pip for outdate requirements."""
    cmd = _build_command('pip')
    logger.info('Checking outdated requirements.')
    invoke.run(f'{cmd} list --outdated')


def _run_isort():
    """Run isort."""
    cmd = _build_command('isort')
    args = '--check-only'
    for cur in _PYTHON_PATHS:
        logger.info('Running isort: %s', cur)
        invoke.run(f'{cmd} {args} {cur}', pty=True)


def _run_pylint():
    """Run pylint."""
    cmd = _build_command('pylint')
    args = ''
    for cur in _PYTHON_PATHS:
        logger.info('Running pylint: %s', cur)
        invoke.run(f'{cmd} {args} {cur}', pty=True)


def _run_flake8():
    """Run flake8."""
    cmd = _build_command('flake8')
    args = ''
    for cur in _PYTHON_PATHS:
        logger.info('Running flake8: %s', cur)
        invoke.run(f'{cmd} {args} {cur}', pty=True)


def _run_pytest():
    """Run pytest."""
    cmd = _build_command('pytest')
    args = ''
    logger.info('Running pytest.')
    invoke.run(f'{cmd} {args}', pty=True)


def _run_pylint_todo_check():
    """Just run the check for "TODO"."""
    cmd = _build_command('pylint')
    args = '--enable W0511 --notes "TODO" --exit-zero --score n'
    for cur in _PYTHON_PATHS:
        logger.info('Running pylint check for TODOs: %s', cur)
        invoke.run(f'{cmd} {args} {cur}', pty=True)


@invoke.task
def test(context):  # pylint: disable=unused-argument
    """Run all of the tests: pip list, isort, pylint, pytest."""
    _check_pip_outdated()
    _run_isort()
    _run_pylint()
    _run_flake8()
    _run_pytest()
    _run_pylint_todo_check()
