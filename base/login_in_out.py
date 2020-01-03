import requests

from StartField.conf.readConfig import Login_User, Login_Password, ReadConfig


def login_in_status(sess):
    url = ReadConfig().get_base_url() +"/eshop/pc/crmMember/login"
    data = {
        "loginName": Login_User,
        "password": Login_Password
    }

    cookie_jar = sess.post(url=url, json=data)
    cookie = cookie_jar.cookies
    cookie_t = requests.utils.dict_from_cookiejar(cookie)   # 把cookis对象 转成字典

    return cookie_t


def login_out_status(sess):
    url = ReadConfig().get_base_url() +"/eshop/pc/crmMember/logout"
    cookie_jar = sess.post(url=url)



if __name__ == '__main__':
    s = requests.session()
    m = login_out_status(s)
    print(m)
    print(s)