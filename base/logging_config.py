# coding=utf-8
import logging
from logging.handlers import RotatingFileHandler

from conf.readConfig import PATH, LOG_level


class Log(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=LOG_level)
        handler = logging.FileHandler(PATH+"/log/log.txt")  # 写入日志文件
        self.handler = RotatingFileHandler(PATH+"/log/log.txt", maxBytes=1024*1024, backupCount=3)  #设置日志回滚，和文件大小、数量
        self.handler.suffix = "%H_%M.log"
        self.handler.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - %(message)s')
        # self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)

        self.console = logging.StreamHandler()
        self.console.setLevel(logging.INFO)
        self.console.setFormatter(self.formatter)

        self.logger.addHandler(self.handler)
        # self.logger.addHandler(self.console)


if __name__ == '__main__':

    logger = Log()
    logger.logger.info("{}".format(__file__))
    # logger.debug("Do something")
    # logger.warning("Something maybe fail.")
    # logger.error("Finish")
