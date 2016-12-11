# -*- coding: utf-8 -*-
__author__ = 'a.oreshko'

from logger.logger import *
from User import User
from App import App

logger = Logger()
logger.write_log("Program started", logger.SYSTEM_FILE_NAME)
user = User()
user.authorization()
app = App(user.driver, logger, user)
app.find_message()










