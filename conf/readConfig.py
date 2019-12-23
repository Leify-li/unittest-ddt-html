#!/usr/bin/python3
# coding=utf-8

import configparser
import os


proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "config.ini")
PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  # 此项目的根目录

class ReadConfig:
    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(configPath,encoding="utf-8")

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

if __name__ == '__main__':
    ws = ReadConfig().get_base_url()
    print(ws)