#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
import sys
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, parseaddr
from conf.readConfig import case_excel_path, result_excel_path, EMail_Server, EMail_Server_Port, result_html_path,Receivers,Receiver , Sender, PassWD,result_html_path
from base.logging_config import Log
logger = Log()

# my_sender = '1253399764@qq.com'  # 发件人邮箱账号
# my_pass = 'sjicwypwgamwhaaf'  # 发件人邮箱密码
# # receivers = '1253399764@qq.com'
# receivers = 'lilingfeng@jiancaiyi.cn'


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

class SendMail(object):

    def __init__(self,sender, passwd, receiver, title, content,
                 receivers = [],
                 file = None,
                 email_host=EMail_Server, port=EMail_Server_Port):
        self.username = sender
        self.passwd = passwd
        self.recv = receiver
        self.receivers = receivers
        self.title = title
        self.content = content
        self.file = file
        self.email_host = email_host
        self.port = port
        self.message = MIMEMultipart()

    def send(self):

        self.message['From'] = _format_addr('测试组 <%s>' % self.username)
        self.message['To'] = _format_addr(' <%s>' % self.recv)
        self.message['Cc'] = _format_addr(' <%s>' % self.receivers)

        self.message['Subject'] = Header(self.title, 'utf-8')



        # if self.file:
        # with open(result_html_path, "rb") as f:
        #     self.content = f.read()

        # 邮件正文内容
        self.message.attach(MIMEText(self.content, 'plain', 'utf-8'))



        att1 = MIMEText(open(result_excel_path, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1["Content-Disposition"] = 'attachment; filename="result.xlsx"'
        self.message.attach(att1)

        # 构造附件2，传送当前目录下的 runoob.txt 文件
        att2 = MIMEText(open(case_excel_path, 'rb').read(), 'base64', 'utf-8')
        att2["Content-Type"] = 'application/octet-stream'
        att2["Content-Disposition"] = 'attachment; filename="test_case.xlsx"'
        self.message.attach(att2)

        att3 = MIMEText(open(result_html_path, 'rb').read(), 'base64', 'utf-8')
        att3["Content-Type"] = 'application/octet-stream'
        att3["Content-Disposition"] = 'attachment; filename="result.html"'
        self.message.attach(att3)

        ret = True
        server = smtplib.SMTP_SSL(self.email_host, self.port)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(self.username, self.passwd)            # 括号中对应的是发件人邮箱账号、邮箱密码
        try:
            self.receivers.append(self.recv)

            server.sendmail(self.username,  self.receivers, self.message.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        except Exception as msg:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            ret = False
            logger.logger.exception(sys.exc_info())
            print("邮件发送失败")
        else:
            print("邮件发送成功")
        finally:
            server.quit()  # 关闭连接

        return ret


if __name__ == '__main__':

    ret = SendMail(Sender, PassWD, Receiver, '接口自动化测试', content="自动化测试：\n   测试用例： test_case.xlsx\n   测试结果： result.xlsx 、result.html ", receivers=Receivers)
    ret = ret.send()
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")