from fixture.orm import ORMFixture
from model.contact import Contact
from model.group import Group
from random import choice


DB = ORMFixture(host="127.0.0.1", name="addressbook", user="root", password="")


def test_del_contact_from_group(app):
    if len(DB.get_contacts_in_groups()) == 0:
        contact = Contact(firstname="1")
        group = Group(name="test")
        app.contact.create(contact)
        app.group.create(group)
        app.contact.add_contact_in_group(contact, group)
    contact = choice(DB.get_contacts_in_groups())
    group = DB.get_contact_group(contact)
    old_contacts = DB.get_contacts_in_group(group)
    app.contact.del_contact_from_group(contact, group)
    new_contacts = DB.get_contacts_in_group(group)
    old_contacts.remove(contact)
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)
