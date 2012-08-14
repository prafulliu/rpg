import logging
import os

class CLog():
	def __init__(self, log_name):
		self._log_name   = log_name
		self._logger     = logging.getLogger(log_name)
		self._screen_log = logging.StreamHandler()
		self._format     = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

		self._screen_log.setFormatter(self._format)	
		self._logger.addHandler(self._screen_log)

	def get_logger(self):
		return self._logger

LOG = CLog('mylog').get_logger()	
LOG.setLevel(logging.DEBUG)

#CRITICAL, ERROR, WARNING, INFO or DEBUG
class CType():
	def __init__(self):
		self.CRITICAL = logging.CRITICAL
		self.ERROR    = logging.ERROR
		self.WARNING  = logging.WARNING
		self.INFO     = logging.INFO
		self.DEBUG    = logging.DEBUG

TYPE = CType()

#	logger = logging.getLogger('mylogger')
#	logger.setLevel(logging.DEBUG)
#	
#	fh = logging.FileHandler('D:\\project\\mycode\\python\\log\\test.log')
#	fh.setLevel(logging.DEBUG)
#	
#	ch = logging.StreamHandler()
#	ch.setLevel(logging.DEBUG)
#	
#	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#	fh.setFormatter(formatter)
#	ch.setFormatter(formatter)
#	
#	logger.addHandler(fh)
#	logger.addHandler(ch)
#	
#	logger.info('foorbar')
