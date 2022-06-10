from pathlib import Path
import environ
import os

env = environ.Env(
    SSH_KEY_PATH=(str, '~/.ssh/id_rsa'),
    GOOGLE_ACCOUNT_FILE=(str, ''),
    MODEL_IDENTIFIER=(str, 'test'),
    BASE_URL=(str, 'host.docker.internal:8000'),
    DB_SSH_URL=(str, ''),
    DB_SSH_USER=(str, ''),
    DB_USER=(str, ''),
    DB_PASSWORD=(str, ''),
    DB_DB=(str, ''),
)

BASE_DIR = Path(os.getcwd()).resolve()


def __reload_variables():
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


def get_variable(name: str):
    __reload_variables()
    return env(name)


def SSH_KEY_PATH():
    __reload_variables()
    return env('SSH_KEY_PATH')


def GOOGLE_ACCOUNT_FILE():
    __reload_variables()
    return env('GOOGLE_ACCOUNT_FILE')


def MODEL_IDENTIFIER():
    __reload_variables()
    return env('MODEL_IDENTIFIER')


def BASE_URL():
    __reload_variables()
    return env('BASE_URL')


def DB_SSH_URL():
    __reload_variables()
    return env('DB_SSH_URL')


def DB_SSH_USER():
    __reload_variables()
    return env('DB_SSH_USER')


def DB_USER():
    __reload_variables()
    return env('DB_USER')


def DB_PASSWORD():
    __reload_variables()
    return env('DB_PASSWORD')


def DB_DB():
    __reload_variables()
    return env('DB_DB')
