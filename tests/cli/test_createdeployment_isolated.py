import os
import shutil

import pytest
from tests.cli.utils import run_cmd

from lilya.app import Lilya

app = Lilya(routes=[])


@pytest.fixture(scope="module")
def create_folders():
    os.chdir(os.path.split(os.path.abspath(__file__))[0])
    try:
        os.remove("app.db")
    except OSError:
        pass
    try:
        shutil.rmtree("deployment")
    except OSError:
        pass
    try:
        shutil.rmtree("temp_folder")
    except OSError:
        pass

    yield

    try:
        os.remove("app.db")
    except OSError:
        pass
    try:
        shutil.rmtree("deployment")
    except OSError:
        pass
    try:
        shutil.rmtree("temp_folder")
    except OSError:
        pass


def _run_asserts():
    assert os.path.isfile("deployment/docker/Dockerfile") is True
    assert os.path.isfile("deployment/gunicorn/gunicorn_conf.py") is True
    assert os.path.isfile("deployment/nginx/nginx.conf") is True
    assert os.path.isfile("deployment/nginx/nginx.json-logging.conf") is True
    assert os.path.isfile("deployment/supervisor/supervisord.conf") is True


def test_create_app_with_env_var(create_folders):
    (o, e, ss) = run_cmd("tests.cli.main:app", "lilya createdeployment myproject")
    assert ss == 0

    _run_asserts()


def test_create_app_without_env_var(create_folders):
    (o, e, ss) = run_cmd("tests.cli.main:app", "lilya createdeployment myproject", is_app=False)
    assert ss == 0

    _run_asserts()


def test_create_app_without_env_var_with_app_flag(create_folders):
    (o, e, ss) = run_cmd(
        "tests.cli.main:app",
        "lilya --app tests.cli.main:app createdeployment myproject",
        is_app=False,
    )
    assert ss == 0

    _run_asserts()
