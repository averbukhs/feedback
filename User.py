__author__ = 'a.oreshko'
# -*- coding: utf-8 -*-
from selenium.webdriver import DesiredCapabilities
from getpass import getpass
from selenium import webdriver

from logger.logger import Logger

import time

class User():
    login_auth = None
    password_auth = None
    driver = None
    logger = None
    authorization_link = 'https://b2b-center.ru/personal/'
    login_form = "login_form"
    const_fatal = -1
    operators = {
        "a.averbukh": [92609, "Aleksandra Averbukh"],
        "yu.gerasimova": [111568, "Julia Gerasimova"],
        "o.karnacheva": [339188, "Oksana Karnacheva"],
        "k.manukyan": [229474, "Karina Manukyan"],
        "Viktor": [7635, "Viktor Pererushev"],
        "i.kosenkova": [144449, "Irina Kosenkova"]

    }

    def __init__(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = ( "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/534.34 (KHTML, like Gecko) Phantomjs/2.0.1 Safari/534.34" )
        self.driver = webdriver.PhantomJS('E:/last/phantomjs.exe',desired_capabilities=dcap,service_args=['--ssl-protocol=any','--ignore-ssl-errors=true'])
        self.logger = Logger()

    def get_operator_id(self, login):
        return self.operators[login][0]

    def get_operator_name(self, login):
        return self.operators[login][1]

    def get_operator_login(self):
        return self.login_auth

    def authorization(self):
        while True:
            self.login_auth = raw_input("Enter login: ")
            self.password_auth = getpass("Enter password: ")
            self.driver.get(self.authorization_link)
            elem_login = self.driver.find_element_by_name("login_form[login]")
            elem_passwd = self.driver.find_element_by_name("login_form[password]")
            elem_submit = self.driver.find_element_by_id("enter_button")
            elem_login.send_keys(self.login_auth)
            elem_passwd.send_keys(self.password_auth)
            elem_submit.click()
            time.sleep(5)
            html = self.driver.page_source
            if html.find('logout-s') != self.const_fatal:
                break
            else:
                self.logger.write_log("Login or password isn't correct.  " + self.login_auth, self.logger.SYSTEM_FILE_NAME)
                print "Auth failure"
        return True
