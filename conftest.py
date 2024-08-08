import pytest
import json
import os.path
from fixture.application import Application

FIXTURE = None
TARGET = None


@pytest.fixture
def app(request):
    global FIXTURE
    global TARGET
    browser = request.config.getoption("--browser")
    if TARGET is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), request.config.getoption("--target"))
        with open(config_file) as f:
            target = json.load(f)
    if FIXTURE is None or not FIXTURE.is_valid():
        FIXTURE = Application(browser=browser, base_url=target["baseUrl"])
    FIXTURE.session.ensure_login(username=target["username"], password=target["password"])
    return FIXTURE


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        FIXTURE.session.ensure_logout()
        FIXTURE.destroy()

    request.addfinalizer(fin)
    return FIXTURE


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")
