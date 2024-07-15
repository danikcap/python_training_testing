# -*- coding: utf-8 -*-
from model.group import Group


def test_modification_group_name(app):
    app.session.login(username="admin", password="secret")
    app.group.modification_first_group(Group(name="New group"))
    app.session.logout()


def test_modification_group_header(app):
    app.session.login(username="admin", password="secret")
    app.group.modification_first_group(Group(header="New header"))
    app.session.logout()
