import unittest
import ddt
import os
import requests
from StartField.excel_casa import write_Excel
from StartField.excel_casa import read_Excel
from . import runmethod
from StartField.conf.readConfig import PATH

curpath = os.path.dirname(os.path.realpath(__file__))
textxlsx = os.path.join(curpath, "demo_api.xlsx")

# 复制文件到test_report目录下
report_path = os.path.join(os.path.dirname(curpath))
reportxlsx = os.path.join(report_path, "test_report/result.xlsx")

# testdata = read_Excel.GetExcelData().dict_data()
data = read_Excel.GetExcelData(PATH + "/excel_casa/data2.xlsx").dict_data()

@ddt.ddt
class Test_api(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.s = requests.session()
        # 登录，如果有的话，则在此登录
        write_Excel.copy_excel(PATH + "/excel_casa/data2.xlsx", reportxlsx)

    @ddt.data(*data)
    def test_api(self,data):
        res = runmethod.send_request(self.s, data)
        runmethod.write_result(res, filename=reportxlsx)

        check = data["checkpoint"]

        res_text = res['text']

        self.assertTrue(check in res_text)

if __name__ == '__main__':
    unittest.main()



