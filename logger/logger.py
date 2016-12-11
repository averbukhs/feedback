__author__ = 'Vitek05'

from time import localtime, strftime

class Logger():
	FILE_NAME = "log.txt"
	SYSTEM_FILE_NAME = "System"

	def get_file_name(self):
		return self.FILE_NAME

	def write_log(self, string, user_name):
		string_to_write = str(Logger.get_current_time() + " - " + user_name + " " + string + "\n")
		with open(self.get_file_name(), "a") as file_handler:
			file_handler.write(string_to_write)

	@staticmethod
	def get_current_time():
		return strftime("%Y-%m-%d %H:%M:%S", localtime())