import sys

import requests
import json
from conf.readConfig import ReadConfig, PATH, case_excel_path
from conf.readConfig import Excel_col
from excel_casa import read_Excel, write_Excel
from base.logging_config import Log
logger = Log()
# logger.logger.info("info")

def send_request(s, data, cookie = None):
    """发送请求"""
    method = data["method"]
    url = ReadConfig().get_base_url() + data["url"]  # 把congfig文件的路由地址和路径组成完整的URL
    try:
        params = eval(data["params"])
    except Exception as msg:
        params = None
        logger.logger.warning(msg)

    try:
        header = eval(data["header"])
        # print("header:%s" % header)
        if cookie != None:
            header = dict(header, **cookie)
            # header.update(cookie)
    except Exception as msg:
        header = None
        logger.logger.warning(msg)



    test_nub = data['case_id']
    print("*******正在执行用例：  %s ---- module:%s  **********  %s" % (test_nub,data["module"], data["description"]))
    print("请求方式：%s, 请求url:%s" % (method, url))
    print("请求头： %s" % header)
    print("请求params：%s" % params)

    # post请求body类型
    type1 = data["type"]

    # try:
    #     # bodydata = eval(data["data"])
    #     bodydata = ast.literal_eval(data["data"])
    #
    # except Exception as msg:
    #     bodydata = {}
    #     logger.logger.warning(msg)
    #
    try:

        bodydata = json.loads(data["data"])
    except Exception as e:
        bodydata = {}
        logger.logger.warning(e)

    # 判断传data数据还是json
    if type1 == "data":
        body = bodydata
    elif type1 == "json":
        body = json.dumps(bodydata)
    else:
        body = bodydata

    print("请求body：%s" % json.loads(body))

    verify = False
    res = {}  # 接受返回数据
    try:
        res["case_id"] = data["case_id"]
        res['rowNum'] = data['rowNum']

        # print(method, url, params, header, body)
        # verify禁用安全请求警告
        response = s.request(method=method, url=url, params=params, headers=header,
                            data=body, verify=verify)

#todo:
        res["statuscode"] = str(response.status_code)  # 状态码转成str     #页面请求失败还是返回状态码200（未解决

        print("expect:", data["expect"])
        print("statuscode:", res["statuscode"])


        res["text"] = response.content.decode("utf-8")
        res["times"] = str(response.elapsed.total_seconds())  # 接口请求时间转str
        if res["statuscode"] != "200":
            res["error"] = res["text"]
        else:
            res["error"] = ""
        res["msg"] = ""
        if data['expect'] in res['text']:
            res["result"] = "pass"
            print("用例测试结果:   %s---->%s" % (test_nub, res["result"]))
        else:
            res['result'] = "fail"
            print("用例测试结果:   %s---->%s" % (test_nub, res["result"]))

        if res['result'] == "fail":
            res["output"] = response.text
            print("returnData:", res["output"], type(res["output"]))
        else:
            res["output"] = ""
        return res
    except Exception as msg:
        res['msg'] = str(msg)
        logger.logger.exception(sys.exc_info())
        print('msg:', msg)
        return res

def write_result(result, filename):     # 可迁移
    row_nub = result['rowNum']
    # 写入statuscode
    wt = write_Excel.Write_excel(filename)
    wt.write(row_nub, Excel_col().statusCode(), result['statuscode'])  # 写入返回状态码statuscode,第8列
    wt.write(row_nub, Excel_col().time(), result['times'])  # 耗时
    wt.write(row_nub, Excel_col().error(), result['error'])  # 状态码非200时的返回信息
    wt.write(row_nub, Excel_col().result(), result['result'])  # 测试结果 pass 还是fail
    wt.write(row_nub, Excel_col().msg(), result['msg'])  # 抛异常
    wt.write(row_nub, Excel_col().output(), result['output'])  # 抛异常


if __name__ == '__main__':
    data = read_Excel.GetExcelData(data_excel_path).dict_data()
    # print(data[25])
    s = requests.session()
    res = send_request(s, data[22])
    write_result(res, filename=PATH+"/test_report/result.xlsx")


