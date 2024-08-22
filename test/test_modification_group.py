# -*- coding: utf-8 -*-
import random

from model.group import Group


def test_modification_group_name(app, db, json_groups):
    if len(db.get_group_list()) == 0:
        app.group.create(Group(name="test"))
    old_groups = db.get_group_list()
    id_group = random.choice(old_groups).id
    group = json_groups
    group.id = id_group
    app.group.modification_group_by_id(id_group, group)
    new_groups = db.get_group_list()
    for k, old_group in enumerate(old_groups):
        if old_group.id == id_group:
            old_groups[k] = group
            break
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)


# def test_modification_group_header(app):
#     if app.group.count() == 0:
#         app.group.create(Group(name="test"))
#     old_groups = app.group.get_group_list()
#     app.group.modification_first_group(Group(header="New header"))
#     new_groups = app.group.get_group_list()
#     assert len(old_groups) == len(new_groups)
