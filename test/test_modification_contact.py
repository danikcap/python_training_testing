# -*- coding: utf-8 -*-
import random

from model.contact import Contact


def test_modification_contact(app, db, json_contacts):
    if len(db.get_contact_list()) == 0:
        app.contact.create(Contact(firstname="3"))
    old_contacts = db.get_contact_list()
    id_contact = random.choice(old_contacts).id
    contact = json_contacts
    contact.id = id_contact
    app.contact.modification_contact_by_id(id_contact, contact)
    new_contacts = db.get_contact_list()
    for k, old_contact in enumerate(old_contacts):
        if old_contact.id == id_contact:
            old_contacts[k] = contact
            break
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)
