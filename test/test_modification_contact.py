# -*- coding: utf-8 -*-
from model.contact import Contact
from random import randrange


def test_modification_contact(app, json_contacts):
    if app.contact.count() == 0:
        app.contact.create(Contact(firstname="3"))
    old_contacts = app.contact.get_contact_list()
    index = randrange(len(old_contacts))
    contact = json_contacts
    contact.id = old_contacts[index].id
    app.contact.modification_contact_by_index(index, contact)
    assert len(old_contacts) == app.contact.count()
    new_contacts = app.contact.get_contact_list()
    old_contacts[index] = contact
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)
