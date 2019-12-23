# coding=utf-8
import unittest
import time
from StartField.HtmlTestRunner.runner import HTMLTestRunner
import os
from StartField.conf.readConfig import PATH

report_path = os.path.join(PATH, 'test_report')
if not os.path.exists(report_path):
    os.mkdir(report_path)
case_path = os.path.join(PATH, "base")

def add_case(casepath=case_path, rule="test*.py"):
    '''加载测试用例'''

    discover = unittest.defaultTestLoader.discover(casepath, pattern=rule,)
    print(discover)
    return discover

def run_case(all_case, reportpath=report_path):

    htmlreport = reportpath+r"\result.html"
    print("测试报告生成地址：", htmlreport)

    fp = open(htmlreport, "wb")
    runner = HTMLTestRunner(output=fp, report_title="测试报告", failfast=True )
    runner.run(all_case)
    fp.close()

if __name__ == '__main__':
    case = add_case(case_path)
    run_case(case)
