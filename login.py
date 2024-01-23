import requests
import subprocess
import json


# 登入类，默认从本地获取cookie登入，失败后使用表单登入
# 接受一个参数：账号
class Login:
    def __init__(self, username):
        self.username = username

        # 读取config.json文件
        try:
            with open("config.json", "r") as file:
                self.config = json.load(file)
        except Exception as e:
            print(f"错误：{e}")

        # 从config.json中读取配置信息
        self.login_url = self.config["url"]["login_form"]
        self.home_url = self.config["url"]["home"]

        # 创建session对象
        self.session = requests.Session()

        # 通过本地存储的cookie登入
        if self.__cookie_login():
            return

        # 通过表单登入
        self.__form_login()

        # 更新cookie到本地
        self.__storage_cookie()

    def getSession(self):
        return self.session

    def __cookie_login(self):
        try:
            with open("cookies.json", "r") as f:
                cookie = json.load(f)[self.username]
        except Exception:
            print(f"读取cookies.json文件失败或当前用户不存在本地cookie")
            return False

        self.session.cookies.update(cookie)
        response = self.session.get(self.home_url)
        if response.status_code != 200:
            return False
        # print("成功通过cookie登入")
        return True

    def __form_login(self):
        with open("user.json", "r") as f:
            self.password = json.load(f)[self.username]["psw"]

        # 配置headers
        self.session.headers.update(self.config["headers"]["login_headers"])

        # 访问登入页，获取原始session
        self.session.get(self.login_url)

        # 获取加密后的密码（本地调用nodejs）
        encrypt_password = "__RSA__" + subprocess.run(["node", "js/login.js", self.password], capture_output=True,
                                                      text=True).stdout

        # 配置登入表单数据
        login_data = self.config["data"]["login_data"]
        login_data["username"] = self.username
        login_data["password"] = encrypt_password

        # 提交登入数据，获取最终的session，并自动重定向到教务系统首页：https://jw.cdut.edu.cn/jsxsd/framework/xsMainV.htmlx
        self.session.post(url=self.login_url, data=login_data)
        print("成功通过表单登入")

    def __storage_cookie(self):
        json_data = {}
        # 读取原cookie数据
        try:
            with open("cookies.json", "r") as f:
                json_data = json.load(f)
        except FileNotFoundError:
            print("文件:cookies.json 未找到")
        except json.decoder.JSONDecodeError as e:
            print("文件:cookies.json读取错误，可能是文件为空")
        except Exception as e:
            print(f"错误：{e}")

        # 添加新的数据
        json_data[self.username] = self.session.cookies.get_dict()
        # 写入
        with open("cookies.json", "w") as f:
            json.dump(json_data, fp=f, indent=2)
