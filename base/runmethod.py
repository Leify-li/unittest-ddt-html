import requests
import json
from StartField.conf.readConfig import ReadConfig, PATH
from StartField.excel_casa import read_Excel, write_Excel


# class RunMethod():
#     def post_main(self,url, data, header=None):
#         res = None
#         if header is not None:
#             res = requests.post(url=url, data=data, header=header)
#         else:
#             res = requests.post(url=url, data=data)
#         return res.json()
#
#     def get_main(self, url, data=None, header=None):
#         res = None
#
#         if header is not None:
#             res = requests.get(url=url, data=data, header=header, verify=False)
#         else:
#             res = requests.get(url=url)
#         return json.dumps(res, ensure_ascii=False, sort_keys=True, indent=2)

def send_request(s, data):
    method = data["method"]
    url = ReadConfig().get_base_url() + data["url"]  # 把congfig文件的路由地址和路径组成完整的URL
    try:
        params = eval(data["params"])
    except:
        params = None

    try:
        header = eval(data["header"])
        print("header:%s" % header)
    except:
        header = None

    test_nub = data['case_id']
    print("*******正在执行用例：-----  %s  ----**********" % test_nub)
    print("请求方式：%s, 请求url:%s" % (method, url))
    print("请求params：%s" % params)

    # post请求body类型
    type = data["type"]
    try:
        bodydata = eval(data["data"])
    except:
        bodydata = {}
    # 判断传data数据还是json

    if type == "data":
        body = bodydata
    elif type == "json":
        body = json.dumps(bodydata)
    else:
        body = bodydata

    verify = False
    res = {}  # 接受返回数据
    try:
        res["case_id"] = data["case_id"]
        res['rowNum'] = data['rowNum']

        print(method, url, params, header, body)
        response = s.request(method=method, url=url, params=params, headers=header,
                            data=body, verify=verify)      # verify禁用安全请求警告
#todo:
        res["statuscode"] = str(response.status_code)  # 状态码转成str     #页面请求失败还是返回状态码200（未解决
        res["text"] = response.content.decode("utf-8")
        res["times"] = str(response.elapsed.total_seconds())  # 接口请求时间转str
        if res["statuscode"] != "200":
            res["error"] = res["text"]
        else:
            res["error"] = ""
        res["msg"] = ""
        # if data['checkpoint'] in res['text']:
        #     res["result"] = "pass"
        #     print("用例测试结果:   %s---->%s" % (test_nub, res["result"]))
        if data['expected'] in res['text']:
            res["result"] = "pass"
            print("用例测试结果:   %s---->%s" % (test_nub, res["result"]))
        else:
            res['result'] = "fail"
        return res
    except Exception as msg:
        res['msg'] = str(msg)
        print('msg:', msg)
        return res

def write_result(result, filename='result.xlsx'):
    row_nub = result['rowNum']
    # 写入statuscode
    wt = write_Excel.Write_excel(filename)
    wt.write(row_nub, 10, result['statuscode'])  # 写入返回状态码statuscode,第8列
    wt.write(row_nub, 11, result['times'])  # 耗时
    wt.write(row_nub, 12, result['error'])  # 状态码非200时的返回信息
    wt.write(row_nub, 14, result['result'])  # 测试结果 pass 还是fail
    wt.write(row_nub, 15, result['msg'])  # 抛异常


if __name__ == '__main__':
    data = read_Excel.GetExcelData(PATH+"/excel_casa/data2.xlsx").dict_data()
    print(data[0])
    s = requests.session()
    res = send_request(s, data[1])
    print(res)
    write_Excel.copy_excel(PATH+"/excel_casa/data2.xlsx", PATH+"/excel_casa/result.xlsx")
    write_result(res, filename=PATH+"/excel_casa/result.xlsx")


