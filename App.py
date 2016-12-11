# -*- coding: utf-8 -*-
__author__ = 'a.oreshko'
# encoding=utf8

import time
from hipster import Hipster
import datetime
from datetime import timedelta

class App():
    driver = None
    logger = None
    username = None
    link = 'https://www.b2b-center.ru/admin/manage_feedback.html?action=search&text_type=&text=' \
           '&firm_id=&gate=&handler%5B%5D=9&operator_id=&category=&type=&status=0&priority=&date_type=0' \
           '&date_start_dmy=%D0%B4%D0%B4.%D0%BC%D0%BC.' \
           '%D0%B3%D0%B3%D0%B3%D0%B3' \
           '&date_end_dmy=%D0%B4%D0%B4.%D0%BC%D0%BC.%D0%B3%D0%B3%D0%B3%D0%B3' \
           '&date_start__date_end__interval='
    start_dmy = 3600
    end_dmy = 10
    const_fatal = -1


    def __init__(self, driver, logger, username):
        self.driver = driver
        self.logger = logger
        self.username = username

    def find_message(self):
        a = ""
        n = 0
        while True:
            self.driver.get(self.link)
            html = self.driver.page_source
            if html.find(u"Всего найдено записей: ") != self.const_fatal:
                i = html.find(u"Всего найдено записей: ")
                s1 = html[i + 42:i + 48] # @todo Вырезаем подстроку с количеством сообщений..
                n = s1.find("</b>")
                result = s1[0:n]
                if a != 1: # @Это флаг, принимающий 3 состояния, на основе него идет отслеживание ситуации с кол-вом сообщений...
                    print u"Увага, новых сообщений ", result
                    r_string = "You have " + result + " messages in feedback B2B-center"
                    self.send_messages(r_string, self.logger)
                    self.logger.write_log(r_string, self.username.login_auth)
                    a = 1
            elif html.find(u"Записей не найдено") != self.const_fatal:
                if a != 0:
                    print u"Гуляй! Сообщений нет! Ты никому не нужен!"
                    r_string = "You haven't messages in feedback B2B-center"
                    self.send_messages(r_string, self.logger)
                    self.logger.write_log(r_string, self.username.login_auth)
                    a = 0
            else:
                if a != 2:
                    print u"Сообщение всего одно!"
                    r_string = "You have 1 message in feedback B2B-center"
                    self.send_messages(r_string, self.logger)
                    self.logger.write_log(r_string, self.username.login_auth)
                    a = 2
            if n == 0:
                self.find_old_messages(self.start_dmy, self.end_dmy)
            n += 1
            if n == 240: #Ведется отсчет 4 часа, и сбрасывается на 0
                n = 0
            time.sleep(60) #Проверяет каждую минуту новые обращения

    def find_old_messages(self, start, end):
        for key in self.username.operators:
            start_dmy = datetime.date.today() - timedelta(days=start)
            end_dmy = datetime.date.today() - timedelta(days=end)
            link = 'https://www.b2b-center.ru/admin/manage_feedback.html?action=search&text_type=&text=&firm_id=&gate=&handler%5B%5D=&operator_id=' + str(
                self.username.get_operator_id(key)) + '&category=&type=&status=3&priority=&date_type=0&date_start_dmy=' + str(
                start_dmy.strftime('%d.%m.%Y')) + '&date_end_dmy=' + str(
                end_dmy.strftime('%d.%m.%Y')) + '&date_start__date_end__interval='

            self.driver.get(link)
            html = self.driver.page_source
            if html.find(u"Всего найдено записей: ") != self.const_fatal:
                i = html.find(u"Всего найдено записей: ")
                s1 = html[i + 23:i + 33]
                n = s1.find("</b>")
                result = s1[0:n]
                print self.username.get_operator_name(key), u" у Вас есть незакрытые сообщения ", result
                r_string = self.username.get_operator_name(key) + " has " + result + " messages in feedback B2B-center older than 10 days "
                self.send_messages(r_string, self.logger)
                self.logger.write_log(r_string, self.username.login_auth)
            elif html.find(u"Записей не найдено") != self.const_fatal:
                pass
            else:
                print self.username.get_operator_name(key), u" у Вас есть одно незакрытое сообщение!"
                r_string = self.username.get_operator_name(key) + " has 1  old message in feedback B2B-center older than 10 days" \
                                                                  ""
                self.send_messages(r_string, self.logger)
                self.logger.write_log(r_string, self.username.login_auth)

    @staticmethod
    def send_messages(message, logger):
        hipchat = Hipster("54810c1fb590765c5253677971af09")
        hipchat.send_messages(
            room_id=673462,
            sender="Eye of Sauron",
            message=message
        )
        logger.write_log("Send message to HipChat: " + message, logger.SYSTEM_FILE_NAME)