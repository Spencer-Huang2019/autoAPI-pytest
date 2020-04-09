import logging

class log(object):
    def __init__(self, filepath):
        self.filepath = filepath

    def msg(self, msg, level):
        # instantiate a logging object
        logger = logging.getLogger()
        # create a logging handler
        handler = logging.FileHandler(self.filepath)
        # define log format
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        # adding format to handler
        handler.setFormatter(formatter)
        # adding handler to logger
        logger.addHandler(handler)
        # set level for logger
        logger.setLevel(logging.DEBUG)

        if level == 'info':
            logger.info(msg)
        elif level == 'debug':
            logger.debug(msg)
        else:
            logger.error(msg)
        logger.removeHandler(handler) #if missing this step, it will cause multiple records for the same msg