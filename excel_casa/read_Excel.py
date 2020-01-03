import xlrd as xlrd
from conf.readConfig import Skip_Case,Skip_model, case_excel_path, Select
import xlwt
from base.logging_config import Log
logger = Log()
logger.logger.info("info")



class GetExcelData():
    """获取Excel数据， 并帅选出不执行的用例"""
    def __init__(self, excel_path, sheetName="Sheet1"):
        self.data = xlrd.open_workbook(excel_path)
        self.table = self.data.sheet_by_name(sheetName)
        self.keys = self.table.row_values(0)  # 获取第一行的key
        self.rowNum = self.table.nrows  # 获取总行数
        self.colNum = self.table.ncols  # 获取总列数

    def dict_data(self):
        if self.rowNum <= 1:
            print("总行数小于1")
        else:
            data = []
            j = 1
            for i in list(range(self.rowNum - 1)):
                dic = {}
                dic['rowNum'] = i+2
                values = self.table.row_values(j)
                for x in list(range(self.colNum)):
                    dic[self.keys[x]] = values[x]
                if Select:
                    if (dic["case_id"]  in (Skip_Case)) or (dic["module"]  in Skip_model):
                        data.append(dic)
                    else:
                        print(dic['case_id'], end=" / ")
                else:
                    data.append(dic)

                j += 1

        return data


if __name__ == '__main__':
    filepath = case_excel_path
    # sheetName = "data"
    data = GetExcelData(filepath).dict_data()
    print(data)
    # print(data[20])
    # print(type(data[20]["module"]))