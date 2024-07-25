# -*- coding: utf-8 -*-
from model.contact import Contact


def test_modification_first_contact(app):
    if app.contact.count() == 0:
        app.contact.create(Contact(firstname="3"))
    old_contacts = app.contact.get_contact_list()
    contact = Contact("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11",
                      "12", "13", "14", "15", "25", "September", "1800", "20",
                      "November", "1700")
    contact.id = old_contacts[0].id
    app.contact.modification_first_contact(contact)
    assert len(old_contacts) == app.contact.count()
    new_contacts = app.contact.get_contact_list()
    old_contacts[0] = contact
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)
