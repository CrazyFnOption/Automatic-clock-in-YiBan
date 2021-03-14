import requests
import re


class YiBan:
    CSRF: "wang-shu-xiao-zui-shuai"
    Cookie: {"csrf_token":CSRF}
    HEADERS = {"Origin": "https://c.uyiban.com", "User-Agent": "yiban"}

    def __init__(self, username, password):
        self.username = username                        # 登陆账号
        self.password =  password                       # 登陆密码
        self.session = requests.session()               # session 保留信息
        self.name = ""                                  # 本人的姓名
        self.imapp=""                                   # 轻应用的id

    def request(self, url, method="get", params=None, cookies=None):
        if method == "get":
            req = self.session.get(url=url, params= params, cookies=cookies, headers=self.HEADERS)
        else:
            req = self.session.post(url, data=params, timeout=10, headers=self.HEADERS, cookies=cookies)
        try:
            return req.json()
        except:
            return None

    def login(self):
            params = {
                "mobile": self.username,
                "imei": "0",
                "password": self.password
            }
            r = self.request(url="https://mobile.yiban.cn/api/v3/passport/login", params=params)
            if r is not None and str(r["response"]) == "100":
                self.access_token = r["data"]["user"]["access_token"]
                return r
            else:
                raise Exception("账号或密码错误")

    def getRootPage(self):
        params = {
            "access_token": self.access_token,
        }
        r = self.request(url="https://mobile.yiban.cn/api/v3/home", params=params)
        self.name = r["data"]["user"]["userName"]
        for i in r["data"]["hotApps"]:                                              #动态取得轻应用id
            if i["name"] == "信息上报":
                self.iapp = re.findall(r"(iapp.*)\?", i["url"])[0]
        return r