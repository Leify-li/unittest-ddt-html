#!/usr/bin/python3
# coding=utf-8

import configparser
import logging
import os
import time




proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "config.ini")
PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  # 此项目的根目录
# result_excel_path = PATH + "/test_report/result_"+NowDate+".xlsx"

report_path = os.path.join(PATH, 'test_report')                          # 测试报告结果的存放路经
if not os.path.exists(report_path):
    os.mkdir(report_path)

result_excel_path = PATH + "/test_report/result.xlsx"                  # excel测试用例结果的存放路经

case_path = os.path.join(PATH, "base")                                  # 测试文件的路径

NowDate = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))  # 当前日期和时间



class ReadConfig:
    def __init__(self):
        #  实例化configParser对象
        self.cf = configparser.ConfigParser()
        self.cf.read(configPath,encoding="utf-8")      # -read读取ini文件


    def get_base_url(self):
        protocol = self.cf.get("HTTP", "protocol")
        # 测试环境
        ip = self.cf.get("HTTP", "ip")
        try:
            port = self.cf.get("HTTP", "port")
        except Exception as e:
            port = ""

        if port == "":
            base_url = protocol + '://' + ip
        else:
            base_url = protocol + '://' + ip + ':' + port
        # 生成环境
        # basics = self.cf.get("HTTP", "basics")
        # base_url = protocol + '://' + basics

        return base_url

    def get_excel(self):
        id1, module1 = [] , []
        a = self.cf.get("Excel", "id")
        a = a.split(',')
        id = map(lambda a: a.strip(), a)
        id = list(id)

        module = self.cf.get("Excel", "module")
        module = module.split(',')
        module = map(lambda a: a.strip(), module)
        module = list(module)
        for i in id:
            if i != '':
                id1.append(i)

        for i in module:

            if i != '':
                module1.append(i)

        select = self.cf.get("Excel", "select")
        if select == "true":
            select = True
        elif select == "false":
            select = False
        else:
            select = False

        return id1, module1, select

    def get_log_level(self):
        level = self.cf.get("log", "level")
        # print(level, type(level))

        if level == '1':
            level = logging.INFO
        elif level == '2':
            level = logging.WARNING
        elif level == '3':
            level = logging.ERROR
        else:
            level = logging.INFO

        return level

    def get_login_user(self):
        user = self.cf.get("HTTP", "user")
        pwd = self.cf.get("HTTP", "password")
        # print(user, pwd)
        return user, pwd


class Excel_col:
    def __init__(self):
        #  实例化configParser对象
        self.cf = configparser.ConfigParser()
        self.cf.read(configPath, encoding="utf-8")  # -read读取ini文件

    def statusCode(self):
        return int(self.cf.get("Excel", 'statusCode'))

    def time(self):
        return int(self.cf.get("Excel", 'time'))

    def error(self):
        return int(self.cf.get("Excel", 'error'))

    def result(self):
        return int(self.cf.get("Excel", 'result'))

    def msg(self):
        return int(self.cf.get("Excel", 'msg'))

    def output(self):
        return int(self.cf.get("Excel", 'output'))

    def test_local(self, local):
        return "/"+self.cf.get("TestCase", local)





case_excel_path = PATH + Excel_col().test_local("local")            # excel测试用例的存放路经

Skip_Case, Skip_model, Select = ReadConfig().get_excel()
LOG_level = ReadConfig().get_log_level()
Login_User, Login_Password = ReadConfig().get_login_user()

if __name__ == '__main__':
    pass
    # ws = ReadConfig()
    # a,b = ws.get_excel()

    # print(list(a), list(b))

