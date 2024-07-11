# -*- coding: utf-8 -*-
from model.group import Group


def test_modification_group(app):
    app.session.login(username="admin", password="secret")
    app.group.modification_first_group(Group(name="1", header="2", footer="3"))
    app.session.logout()
