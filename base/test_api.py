import sys
import traceback
import unittest
import warnings
import ddt
import os
import requests

from base.login_in_out import login_in_status, login_out_status
from excel_casa import write_Excel
from excel_casa import read_Excel
from base import runmethod
from conf.readConfig import case_excel_path, result_excel_path, NowDate, PATH
from base.logging_config import Log
logger = Log()
logger.logger.info("info")


data = read_Excel.GetExcelData(case_excel_path).dict_data()
write_Excel.copy_excel(case_excel_path, result_excel_path)  # copy 到test_report路径下


@ddt.ddt
class Test_api(unittest.TestCase):


    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)  # 这行代码的作用是忽略一些告警打印
        self.s = requests.session()
        # 登录，如果有的话，则在此登录
        self.login = False


    @ddt.data(*data)
    def test_api(self, data):
        cookie = None
        # print(type(data["token"]))
        if data["token"] != 0:
            self.login = True
            cookie = login_in_status(self.s)       # 获取登录状态的token
            print("Login_in")

        res = runmethod.send_request(self.s, data, cookie)
        runmethod.write_result(res, filename=result_excel_path)

        check = data["expect"]
        res_text = res['text']
        # print(check, res_text)
        # print(res_text)

        self.assertTrue(check in res_text, msg="expect 检出错误")
        self.assertEqual(res["statuscode"], '200', msg="error")
        # logger.logger.exception(sys.exc_info())
        # logger.logger.error('error!', exc_info=True)

    def tearDown(self) -> None:
        if self.login:
            print("Logout")
            login_out_status(self.s)


if __name__ == '__main__':
    unittest.main()



