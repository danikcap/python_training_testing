# -*- coding: utf-8 -*-
from model.contact import Contact


def test_add_contact(app):
    app.session.login(username="admin", password="secret")
    app.contact.create(Contact("asd", "asd", "asd", "asd", "asd", "asd", "asd", "asd", "asd", "asd", "asd",
                               "asd", "asd", "asd", "asd", "27", "September", "1900", "26", "November", "1900"))
    app.session.logout()
