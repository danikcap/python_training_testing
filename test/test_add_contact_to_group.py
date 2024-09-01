from random import choice
from fixture.orm import ORMFixture
from model.contact import Contact
from model.group import Group


DB = ORMFixture(host="127.0.0.1", name="addressbook", user="root", password="")


def test_add_contact_to_group(app):
    if len(DB.get_group_list()) == 0:
        app.group.create(Group(name="test"))
    if len(DB.get_contacts_not_in_groups()) == 0:
        app.contact.create(Contact(firstname="1"))
    group_list = DB.get_group_list()
    group = choice(group_list)
    contact_list = DB.get_contacts_not_in_groups()
    contact = choice(contact_list)
    old_contacts = DB.get_contacts_in_group(group)
    app.contact.add_contact_in_group(contact, group)
    new_contacts = DB.get_contacts_in_group(group)
    old_contacts.append(contact)
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)
