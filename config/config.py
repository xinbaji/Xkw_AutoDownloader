import os
import json
import shutil
from utils.log import Log
from utils.encrypt import usnmdcfiiro1cqqt, pwdcfiiro1c


class Config:
    def __init__(self) -> None:
        self.log = Log("config", "i")

        if os.path.exists("./download") == False:
            os.makedirs("download")
            os.makedirs("tasks", exist_ok=True)
            os.makedirs("env", exist_ok=True)
            os.makedirs("temp", exist_ok=True)

        if not os.path.exists("./config/config.json"):
            self.config = {
                "send_from_email": "",
                "username": "",
                "password": "",
                "code": "",
                "driver": "",
            }

        else:
            with open("./config/config.json", "r") as f:
                self.config = json.load(f)
                f.close()

        if self.username() is None:
            self.get_username_and_password()

            try:
                shutil.rmtree("./env")
            except Exception as e:
                self.log.debug("无法删除目录或目录不存在：Exception:" + str(e))
            os.makedirs("env", exist_ok=True)

    def get_username_and_password(self):
        username = input("请输入用户名（按回车键确认）：")
        password = input("请输入密码（按回车键确认）：")
        send_from_email = input("请输入发送者的邮箱（按回车键确认）：")
        code = input("请输入授权码（按回车键确认）：")
        self.add_encrypted_val("code", code)
        self.add_encrypted_val("username", username)
        self.add_encrypted_val("password", password)
        self.add_encrypted_val("send_from_email", send_from_email)
        self.save_to_config_file()

    def code(self):
        if self.config["code"] == "":
            return None
        else:
            return self.get_encryed_val(self.config["code"])

    def send_from_email(self):
        if self.config["send_from_email"] == "":
            return None
        else:
            return self.get_encryed_val(self.config["send_from_email"])

    def username(self):
        if self.config["username"] == "":
            return None
        else:
            return self.get_encryed_val(self.config["username"])

    def password(self):
        if self.config["password"] == "":
            return None
        else:
            return self.get_encryed_val(self.config["password"])

    def save_to_config_file(self):
        with open("./config/config.json", "w") as f:
            f.write(json.dumps(self.config))
            f.close()

    def get(self, key):
        return self.config[key]

    def add_encrypted_val(self, key, value):
        self.config[key] = usnmdcfiiro1cqqt(value)

    def get_encryed_val(self, str):
        return pwdcfiiro1c(str)

    def default_driver(self):
        try:
            if self.config["driver"] == "":
                return None
            else:
                return self.config["driver"]
        except KeyError:
            self.add("driver", "")
            return None

    def add(self, key, value):
        self.config[key] = value
        self.save_to_config_file()
