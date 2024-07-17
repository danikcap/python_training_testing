import pytest
from fixture.application import Application

FIXTURE = None


@pytest.fixture
def app():
    global FIXTURE
    if FIXTURE is None:
        FIXTURE = Application()
    else:
        if not FIXTURE.is_valid():
            FIXTURE = Application()
    FIXTURE.session.ensure_login(username="admin", password="secret")
    return FIXTURE


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        FIXTURE.session.ensure_logout()
        FIXTURE.destroy()

    request.addfinalizer(fin)
    return FIXTURE
