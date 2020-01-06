import sys
import unittest
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.dirname(current_directory) + os.path.sep + ".")
sys.path.append(root_path)

from base.test_html import run_case
from conf.readConfig import PATH, Sender, PassWD, Receivers, Receiver
from base.logging_config import Log
from base.send_email import SendMail


logger = Log()
logger.logger.info("main")


case_path = os.path.join(PATH, "base")


def add_case(casepath=case_path, rule="test*.py"):
    '''加载测试用例'''

    discover = unittest.defaultTestLoader.discover(casepath, pattern=rule)
    return discover


def run():

    run_case(add_case())
    send_mail = SendMail(Sender, PassWD, Receiver,
                         title='接口自动化测试', content="自动化测试：\n   测试用例： test_case.xlsx\n   测试结果： result.xlsx 、result.html \n 佳娥，邮件的内容是这样的OK吗？",
                         receivers=Receivers)
    send_mail.send()


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        logger.logger.exception(sys.exc_info())

    logger.logger.info("process end")
