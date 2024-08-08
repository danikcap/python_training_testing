import pytest
import json
from fixture.application import Application

FIXTURE = None
TARGET = None


@pytest.fixture
def app(request):
    global FIXTURE
    global TARGET
    browser = request.config.getoption("--browser")
    if TARGET is None:
        with open(request.config.getoption("--target")) as config_file:
            target = json.load(config_file)
    if FIXTURE is None or FIXTURE.is_valid():
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
