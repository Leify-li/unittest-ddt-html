import sys
import unittest
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.dirname(current_directory) + os.path.sep + ".")
sys.path.append(root_path)

from base.test_html import run_case
from conf.readConfig import PATH
from base.logging_config import Log


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
