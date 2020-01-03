import sys

from StartField.base.test_html import run_case
import unittest
import os
from StartField.conf.readConfig import PATH
from StartField.base.logging_config import Log
logger = Log()
logger.logger.info("main")


case_path = os.path.join(PATH, "base")


def add_case(casepath=case_path, rule="test*.py"):
    '''加载测试用例'''

    discover = unittest.defaultTestLoader.discover(casepath, pattern=rule)
    return discover


def run():

    run_case(add_case())


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        logger.logger.exception(sys.exc_info())

    logger.logger.info("process end")
