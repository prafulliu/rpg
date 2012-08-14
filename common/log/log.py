import logging
import os

def get_log_path(log_name):
	log_path = os.environ['PYTHONPATH']
	log_path = log_path[1:]
	end = log_path.index('common')
	log_path = log_path[:end]+'log/'+log_name+'.log'
	return log_path

class CLog():
	def __init__(self, log_name):
		self._log_name   = log_name
		self._log_path   = get_log_path(log_name) 
		self._logger     = logging.getLogger(log_name)
		self._file_log   = logging.FileHandler(self._log_path, 'a')
		self._screen_log = logging.StreamHandler()
		self._format     = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

		self._file_log.setFormatter(self._format)	
		self._screen_log.setFormatter(self._format)	
		self._logger.addHandler(self._file_log)
		self._logger.addHandler(self._screen_log)

	def setLevel(self, level):
		self._logger.setLevel(level)
		self._file_log.setLevel(level)
		self._screen_log.setLevel(level)

	def get_logger(self):
		return self._logger

if __name__ == '__main__':
	LOG = CLog('playerlog').get_logger()	
	LOG.setLevel(logging.DEBUG)
	LOG.info('this is a log test %s' % ('new log'))

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
