import xlrd as xlrd
import xlwt


class GetExcelData():
    def __init__(self, excel_path, sheetName="data"):
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
                data.append(dic)
                j += 1
        return data


if __name__ == '__main__':
    filepath = 'data2.xlsx'
    sheetName = "data"
    data = GetExcelData(filepath, sheetName)
    print(data.dict_data())