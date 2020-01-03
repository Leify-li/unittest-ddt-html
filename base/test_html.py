# coding=utf-8
import unittest
import time
from base import HTMLTestRunner
import os
from conf.readConfig import NowDate,report_path, case_path
from base.logging_config import Log
logger = Log()
logger.logger.info("info")


def add_case(casepath=case_path, rule="test*.py"):
    '''加载测试用例'''

    discover = unittest.defaultTestLoader.discover(casepath, pattern=rule,)
    # print("dis",discover)
    return discover

def run_case(all_case, reportpath=report_path):

    # 生成的文件加上日期--到秒
    # htmlreport = reportpath+r"\result_"+NowDate+".html"
    htmlreport = reportpath+r"\result.html"
    # print("测试报告生成地址：", htmlreport)

    fp = open(htmlreport, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(fp=fp, verbosity=2, title="测试报告")
    runner.run(all_case)
    fp.close()


if __name__ == '__main__':
    case = add_case(case_path)
    run_case(case)
