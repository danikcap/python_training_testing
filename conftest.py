import pytest
from fixture.application import Application

FIXTURE = None


@pytest.fixture
def app(request):
    global FIXTURE
    browser = request.config.getoption("--browser")
    base_url = request.config.getoption("--baseUrl")
    if FIXTURE is None:
        FIXTURE = Application(browser=browser, base_url=base_url)
    else:
        if not FIXTURE.is_valid():
            FIXTURE = Application(browser=browser, base_url=base_url)
    FIXTURE.session.ensure_login(username="admin", password="secret")
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
    parser.addoption("--baseUrl", action="store", default="http://localhost/addressbook/")
