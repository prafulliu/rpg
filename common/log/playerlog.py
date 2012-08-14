from log import CLog
import logging
LOG = CLog('playerlog').get_logger()	
LOG.setLevel(logging.DEBUG)

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
