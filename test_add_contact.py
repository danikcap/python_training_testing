# -*- coding: utf-8 -*-
import pytest

from contact import Contact
from application import Application


@pytest.fixture
def app(request):
    fixture = Application()
    request.addfinalizer(fixture.destroy)
    return fixture


def test_add_contact(app):
    app.login(username="admin", password="secret")
    app.create_new_contact(Contact("asd", "asd", "asd", "asd", "asd", "asd", "asd", "asd", "asd", "asd", "asd",
                                   "asd", "asd", "asd", "asd", "27", "September", "1900", "26", "November", "1900"))
    app.logout()
