import logging
import logging.config
import os
import sys

def get_this_dir():
    module = sys.modules[__name__]
    this_dir = os.path.dirname(os.path.abspath(module.__file__))
    return(this_dir)
    
def get_mylog():
    LOG_FILE_NAME = os.path.join("/Users/hpiwowar/Documents/Projects/JDAPsurvey/contact_corresponding", "contact_corresponding.log")
    print(LOG_FILE_NAME)

    logging.getLogger('')
        
    # create logger
    logger = logging.getLogger("simple_example")
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s %(filename)s %(funcName)s %(levelname)-8s %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
    
    # create file handler
    filehandler = logging.handlers.RotatingFileHandler(
              LOG_FILE_NAME, maxBytes=2000000000, backupCount=5)
    filehandler.setLevel(logging.DEBUG)
    
    # add formatter to filehandler
    filehandler.setFormatter(formatter)

    logger.addHandler(filehandler)
    return(logger)
    
# Setup up the public name of the logging handler
log = get_mylog()

