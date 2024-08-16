import pytest
import json
import os.path
import importlib
import jsonpickle

from fixture.application import Application
from fixture.db import DbFixture

FIXTURE = None
TARGET = None


def load_config(file):
    global TARGET
    if TARGET is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            TARGET = json.load(f)
    return TARGET


@pytest.fixture
def app(request):
    global FIXTURE
    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--target"))["web"]
    if FIXTURE is None or not FIXTURE.is_valid():
        FIXTURE = Application(browser=browser, base_url=web_config["baseUrl"])
    FIXTURE.session.ensure_login(username=web_config["username"], password=web_config["password"])
    return FIXTURE


@pytest.fixture(scope="session")
def db(request):
    db_config = load_config(request.config.getoption("--target"))["db"]
    dbfixture = DbFixture(host=db_config["host"], name=db_config["name"], user=db_config["user"], password=db_config["password"])
    def fin():
        dbfixture.destroy()
    request.addfinalizer(fin)
    return dbfixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        FIXTURE.session.ensure_logout()
        FIXTURE.destroy()

    request.addfinalizer(fin)
    return FIXTURE


@pytest.fixture()
def check_ui(request):
    return request.config.getoption("--check_ui")


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")
    parser.addoption("--check_ui", action="store_true")


def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])
        elif fixture.startswith("json_"):
            testdata = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])


def load_from_module(module):
    return importlib.import_module(f"data.{module}").testdata


def load_from_json(file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"data/{file}.json")) as f:
        return jsonpickle.decode(f.read())
