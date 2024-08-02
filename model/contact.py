import random
import string

from sys import maxsize


class Contact:
    def __init__(self, firstname=None, middlename=None, lastname=None, nickname=None, title=None, company=None,
                 address=None, home_phone=None, mobile_phone=None, work_phone=None, fax=None, email=None,
                 email2=None, homepage=None, email3=None, bday=None, bmonth=None, byear=None, aday=None,
                 amonth=None, ayear=None, id=None, all_phones_from_home_page=None, all_emails=None):
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.nickname = nickname
        self.title = title
        self.company = company
        self.address = address
        self.home_phone = home_phone
        self.mobile_phone = mobile_phone
        self.work_phone = work_phone
        self.fax = fax
        self.email = email
        self.email2 = email2
        self.homepage = homepage
        self.email3 = email3
        self.bday = bday
        self.bmonth = bmonth
        self.byear = byear
        self.aday = aday
        self.amonth = amonth
        self.ayear = ayear
        self.id = id
        self.all_phones_from_home_page = all_phones_from_home_page
        self.all_emails = all_emails

    def __repr__(self):
        return f"{self.id}:{self.lastname}:{self.firstname}"

    def __eq__(self, other):
        return (self.id == other.id or self.id is None or other.id is None)\
               and self.lastname == other.lastname and self.firstname == other.firstname

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize

    def get_random(self):
        def random_string(prefix, maxlen):
            symbols = string.ascii_letters + string.digits + " "
            return prefix + "".join([random.choice(symbols) for _ in range(random.randrange(maxlen))])

        self.firstname = random_string("firstname", 5)
        self.middlename = random_string("middlename", 5)
        self.lastname = random_string("lastname", 5)
        self.nickname = random_string("nickname", 5)
        self.title = random_string("title", 5)
        self.company = random_string("company", 5)
        self.address = random_string("address", 5)
        self.home_phone = random_string("home_phone", 5)
        self.mobile_phone = random_string("mobile_phone", 5)
        self.work_phone = random_string("work_phone", 5)
        self.fax = random_string("fax", 5)
        self.email = random_string("email", 5)
        self.email2 = random_string("email2", 5)
        self.homepage = random_string("homepage", 5)
        self.email3 = random_string("email3", 5)

        months = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December")
        self.bday = str(random.randrange(1, 32))
        self.bmonth = random.choice(months)
        self.byear = str(random.randrange(0, maxsize))
        self.aday = str(random.randrange(1, 32))
        self.amonth = random.choice(months)
        self.ayear = str(random.randrange(0, maxsize))
        return self
