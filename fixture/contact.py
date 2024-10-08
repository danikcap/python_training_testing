import re
import pytest

from selenium.webdriver.support.ui import Select
from model.contact import Contact


class ContactHelper:
    def __init__(self, app):
        self.app = app
        self.contact_cache = None

    def fill_contact_form(self, contact):
        wd = self.app.wd
        self.change_field_value("firstname", contact.firstname)
        self.change_field_value("middlename", contact.middlename)
        self.change_field_value("lastname", contact.lastname)
        self.change_field_value("nickname", contact.nickname)
        self.change_field_value("title", contact.title)
        self.change_field_value("company", contact.company)
        self.change_field_value("address", contact.address)
        self.change_field_value("home", contact.home_phone)
        self.change_field_value("mobile", contact.mobile_phone)
        self.change_field_value("work", contact.work_phone)
        self.change_field_value("fax", contact.fax)
        self.change_field_value("email", contact.email)
        self.change_field_value("email2", contact.email2)
        self.change_field_value("homepage", contact.homepage)
        self.change_field_value("email3", contact.email3)
        self.change_dropdown_value("bday", contact.bday)
        self.change_dropdown_value("bmonth", contact.bmonth)
        self.change_field_value("byear", contact.byear)
        self.change_dropdown_value("aday", contact.aday)
        self.change_dropdown_value("amonth", contact.amonth)
        self.change_field_value("ayear", contact.ayear)

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def change_dropdown_value(self, dropdown_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(dropdown_name).click()
            Select(wd.find_element_by_name(dropdown_name)).select_by_visible_text(text)

    def create(self, contact):
        wd = self.app.wd
        # init new contact creation
        self.open_add_contact_page()
        # fill contact form
        self.fill_contact_form(contact)
        # submit contact creation
        wd.find_element_by_xpath("//div[@id='content']/form/input[20]").click()
        self.app.return_to_home_page()
        self.contact_cache = None

    def open_add_contact_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/edit.php") and len(wd.find_elements_by_name("submit")) > 0):
            wd.find_element_by_link_text("add new").click()

    def delete_first_contact(self):
        self.delete_contact_by_index(0)

    def delete_contact_by_index(self, index):
        wd = self.app.wd
        self.app.open_home_page()
        # select contact
        wd.find_elements_by_name("selected[]")[index].click()
        # submit deletion
        wd.find_element_by_css_selector('[value="Delete"]').click()
        self.app.open_home_page()
        self.contact_cache = None

    def delete_contact_by_id(self, id):
        wd = self.app.wd
        self.app.open_home_page()
        # select contact
        wd.find_element_by_css_selector(f"input[value='{id}'").click()
        # submit deletion
        wd.find_element_by_css_selector('[value="Delete"]').click()
        self.app.open_home_page()
        self.contact_cache = None

    def modification_first_contact(self, contact):
        self.modification_contact_by_index(0, contact)

    def modification_contact_by_index(self, index, contact):
        wd = self.app.wd
        self.open_contact_to_edit_by_index(index)
        # fill contact form
        self.fill_contact_form(contact)
        # submit update
        wd.find_element_by_name("update").click()
        self.app.return_to_home_page()
        self.contact_cache = None

    def modification_contact_by_id(self, id, contact):
        wd = self.app.wd
        self.open_contact_to_edit_by_id(id)
        # fill contact form
        self.fill_contact_form(contact)
        # submit update
        wd.find_element_by_name("update").click()
        self.app.return_to_home_page()
        self.contact_cache = None

    def open_contact_to_edit_by_index(self, index):
        wd = self.app.wd
        self.app.open_home_page()
        row = wd.find_elements_by_name("entry")[index]
        cell = row.find_elements_by_tag_name("td")[7]
        cell.find_element_by_tag_name("a").click()

    def open_contact_to_edit_by_id(self, id):
        wd = self.app.wd
        self.app.open_home_page()
        for row in wd.find_elements_by_name("entry"):
            if row.find_elements_by_css_selector(f"input[id='{id}']"):
                cell = row.find_elements_by_tag_name("td")[7]
                cell.find_element_by_tag_name("a").click()
                break
        else:
            pytest.fail("Incorrect id")

    def open_contact_view_by_index(self, index):
        wd = self.app.wd
        self.app.open_home_page()
        row = wd.find_elements_by_name("entry")[index]
        cell = row.find_elements_by_tag_name("td")[6]
        cell.find_element_by_tag_name("a").click()

    def count(self):
        wd = self.app.wd
        self.app.open_home_page()
        return len(wd.find_elements_by_name("selected[]"))

    def get_contact_list(self):
        if self.contact_cache is None:
            wd = self.app.wd
            self.app.open_home_page()
            self.contact_cache = []
            for row in wd.find_elements_by_name("entry"):
                cells = row.find_elements_by_tag_name("td")
                id = cells[0].find_element_by_name("selected[]").get_attribute("value")
                last_name = cells[1].text
                firts_name = cells[2].text
                address = cells[3].text
                all_emails = cells[4].text
                all_phones = cells[5].text
                self.contact_cache.append(Contact(lastname=last_name, firstname=firts_name, address=address, id=id,
                                                  all_emails=all_emails, all_phones_from_home_page=all_phones))
        return list(self.contact_cache)

    def get_contact_info_from_edit_page(self, index):
        wd = self.app.wd
        self.open_contact_to_edit_by_index(index)
        firstname = wd.find_element_by_name("firstname").get_attribute("value")
        lastname = wd.find_element_by_name("lastname").get_attribute("value")
        address = wd.find_element_by_name("address").get_attribute("value")
        id = wd.find_element_by_name("id").get_attribute("value")
        home_phone = wd.find_element_by_name("home").get_attribute("value")
        work_phone = wd.find_element_by_name("work").get_attribute("value")
        mobile_phone = wd.find_element_by_name("mobile").get_attribute("value")
        email = wd.find_element_by_name("email").get_attribute("value")
        email2 = wd.find_element_by_name("email2").get_attribute("value")
        email3 = wd.find_element_by_name("email3").get_attribute("value")
        return Contact(firstname=firstname, lastname=lastname, id=id, home_phone=home_phone, mobile_phone=mobile_phone,
                       work_phone=work_phone, address=address, email=email, email2=email2, email3=email3)

    def get_contact_info_from_view_page(self, index):
        wd = self.app.wd
        self.open_contact_view_by_index(index)
        text = wd.find_element_by_id("content").text
        home_phone = re.search("H: (.*)", text).group(1)
        work_phone = re.search("W: (.*)", text).group(1)
        mobile_phone = re.search("M: (.*)", text).group(1)
        return Contact(home_phone=home_phone, mobile_phone=mobile_phone, work_phone=work_phone)

    def add_contact_in_group(self, contact, group):
        wd = self.app.wd
        self.app.open_home_page()
        wd.find_element_by_css_selector(f"input[value='{contact.id}'").click()
        self.change_dropdown_value("to_group", group.name)
        wd.find_element_by_name("add").click()
        self.app.open_home_page()

    def del_contact_from_group(self, contact, group):
        wd = self.app.wd
        self.app.open_home_page()
        self.change_dropdown_value("group", group.name)
        wd.find_element_by_css_selector(f"input[value='{contact.id}'").click()
        wd.find_element_by_name("remove").click()
        self.app.open_home_page()
