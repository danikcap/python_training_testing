# -*- coding: utf-8 -*-
import pytest

from model.contact import Contact
from fixture.application import Application


@pytest.fixture
def app(request):
    fixture = Application()
    request.addfinalizer(fixture.destroy)
    return fixture


def test_add_contact(app):
    app.session.login(username="admin", password="secret")
    app.contact.create(Contact("asd", "asd", "asd", "asd", "asd", "asd", "asd", "asd", "asd", "asd", "asd",
                               "asd", "asd", "asd", "asd", "27", "September", "1900", "26", "November", "1900"))
    app.session.logout()
