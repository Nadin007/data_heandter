import logging

logger = logging.getLogger('logger_1')

logger.setLevel(logging.DEBUG)
handler_1 = logging.FileHandler('logger_1.log')
format_1 = logging.Formatter('%(name)s -  %(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
handler_1.setFormatter(format_1)
logger.addHandler(handler_1)
