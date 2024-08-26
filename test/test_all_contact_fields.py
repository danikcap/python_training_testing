import re

from random import randrange
from model.contact import Contact


def test_all_contact_fields(app, db):
    if len(db.get_contact_list()) == 0:
        app.contact.create(Contact("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
                                   "25", "September", "1800", "20", "November", "1700"))
    contact_from_db = sorted(db.get_contact_list(), key=Contact.id_or_max)
    contact_from_home_page = sorted(app.contact.get_contact_list(), key=Contact.id_or_max)
    for i in range(len(db.get_contact_list())):
        assert contact_from_home_page[i].lastname == contact_from_db[i].lastname
        assert contact_from_home_page[i].firstname == contact_from_db[i].firstname
        assert contact_from_home_page[i].address == contact_from_db[i].address
        assert contact_from_home_page[i].all_emails == merge_emails_like_on_home_page(contact_from_db[i])
        assert contact_from_home_page[i].all_phones_from_home_page == merge_phones_like_on_home_page(
            contact_from_db[i])


def test_all_random_contact_fields(app):
    contact_count = app.contact.count()
    if contact_count == 0:
        app.contact.create(Contact("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
                                   "25", "September", "1800", "20", "November", "1700"))
        contact_count = 1
    index = randrange(contact_count)
    contact_from_home_page = app.contact.get_contact_list()[index]
    contact_from_edit_page = app.contact.get_contact_info_from_edit_page(index)
    assert contact_from_home_page.lastname == contact_from_edit_page.lastname
    assert contact_from_home_page.firstname == contact_from_edit_page.firstname
    assert contact_from_home_page.address == contact_from_edit_page.address
    assert contact_from_home_page.all_emails == merge_emails_like_on_home_page(contact_from_edit_page)
    assert contact_from_home_page.all_phones_from_home_page == merge_phones_like_on_home_page(contact_from_edit_page)


def merge_emails_like_on_home_page(contact):
    return "\n".join(filter(lambda x: x != "",
                            filter(lambda x: x is not None,
                                   [contact.email, contact.email2, contact.email3])))


def clear(s):
    return re.sub("[() -]", "", s)


def merge_phones_like_on_home_page(contact):
    return "\n".join(filter(lambda x: x != "",
                            map(lambda x: clear(x),
                                filter(lambda x: x is not None,
                                       [contact.home_phone, contact.mobile_phone, contact.work_phone]))))
