# -*- coding: utf-8 -*-
from model.contact import Contact


def test_modification_first_contact(app):
    app.contact.modification_first_contact(Contact("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11",
                                                   "12", "13", "14", "15", "25", "September", "1800", "20",
                                                   "November", "1700"))
