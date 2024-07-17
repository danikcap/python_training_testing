# -*- coding: utf-8 -*-
from model.group import Group


def test_modification_group_name(app):
    app.group.modification_first_group(Group(name="New group"))


def test_modification_group_header(app):
    app.group.modification_first_group(Group(header="New header"))
