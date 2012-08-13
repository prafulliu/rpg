import logging
import logconfig

class CLog()
    def __init__(self, log_name)
        self._log_name = log_name
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

logpath = logconfig.LOGPATH
fh = logging.FileHandler('D:\\project\\mycode\\python\\log\\test.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

logger.info('foorbar')
