import os
import json
import shutil
import yagmail

from time import sleep
from smtplib import SMTPSenderRefused

from utils.log import Log
from utils.encrypt import pwdcfiiro1c, usnmdcfiiro1cqqt
from utils.selenium_driver import Driver
from data.path import Xpath, Css
from config.config import Config


class Xkw:
    def __init__(self) -> None:
        # 初始化 检测config内的用于下载的账号密码，若没有要求用户手动输入。

        self.config = Config()

        # 检测download文件夹
        if os.path.exists("./download") == False:
            os.makedirs("download")
            os.makedirs("tasks", exist_ok=True)
            os.makedirs("env", exist_ok=True)
            os.makedirs("temp", exist_ok=True)

        self.xpath = Xpath()
        self.css = Css()
        self.log = Log("main", "i")

    def login(self):

        self.driver.wait_to_be_visible(self.css.login_button()).click()
        self.driver.wait_to_be_visible(self.xpath.login_switch_button())
        sleep(5)
        self.driver.wait_to_be_visible(self.xpath.login_switch_button()).click()
        print(self.config.get_encryed_val(self.config.username()))
        print(self.config.get_encryed_val(self.config.password()))
        self.driver.wait_to_be_visible(self.xpath.login_username_input()).send_keys(
            self.config.username()
        )
        self.driver.wait_to_be_visible(self.xpath.login_password_input()).send_keys(
            self.config.password()
        )
        self.driver.wait_to_be_visible(self.xpath.login_commit_button()).click()
        self.driver.refresh()
        self.driver.driver.implicitly_wait(60)
        self.config.save_to_config_file()

        # 登录成功，保存登录状态信息
        with open(".\\env\\Login_ok.txt", "w") as f:
            f.close()

    def download(self, url):

        # 检测是否登录

        self.driver.get(url)
        self.driver.driver.implicitly_wait(60)
        if os.path.exists(".\\env\\Login_ok.txt") == False:
            self.login()
        self.driver.wait_to_be_visible(self.xpath.ppt_download_button())
        self.driver.force_click(self.xpath.ppt_download_button())
        self.driver.switch_to_iframe(self.xpath.download_iframe())
        self.driver.wait_to_be_clickable(self.xpath.download_confirm_button())
        sleep(2)
        self.driver.wait_to_be_clickable(self.xpath.download_confirm_button()).click()
        sleep(20)
        # TODO:文件下载状态检测
        self.driver.get("https://www.zxxk.com/")

    def get_filelist(self):
        while True:
            count = 0
            filelist = os.listdir(".\download")
            if len(filelist) != 0:
                for i in range(0, len(filelist), 1):
                    if "cr" in filelist[i]:
                        self.log.info("下载未完成")
                        sleep(5)
                        break
                    else:
                        filelist[i] = ".\\download\\" + filelist[i]
                        count += 1
                if count == len(filelist):
                    return filelist

    def send_yagmail(self, recipientAddrs):

        yag_server = yagmail.SMTP(
            user=self.config.send_from_email(),
            password=self.config.code(),
            host="smtp.qq.com",
        )
        email_to = [
            recipientAddrs,
        ]
        email_attachment_list = self.get_filelist()
        email_title = (
            email_attachment_list[0].replace(".\\download\\", "") + "等文件 (自动发送）"
        )
        email_content = "您的资料已发送，请查收哦~"

        yag_server.send(email_to, email_title, email_content, email_attachment_list)
        self.log.info("发送成功！")
        yag_server.close()

    def update_status(self, status):
        with open("./tasks/status.json", "w") as f:
            json.dump(status, f)
            f.close()

    def get_task(self):
        self.log.info("开始检测任务队列")
        download_location = os.path.join(os.getcwd(), "temp")
        prefs = {"download.default_directory": download_location}
        self.driver = Driver(prefs)
        self.update_status("done")
        while True:
            if os.path.exists("./tasks/task.json") == True:
                with open("./tasks/task.json", "r") as f:
                    task = json.load(f)
                    f.close()
                os.remove("./tasks/task.json")
                self.update_status("busy")

                for i in task["task"]:
                    self.download(i)
                filelist = self.get_filelist()
                if task["recv_email"] != "":
                    try:
                        self.send_yagmail(task["recv_email"])

                    except SMTPSenderRefused as sr:
                        self.log.error("Message too large.")

                else:
                    for f in os.listdir(".\\temp"):
                        shutil.move(
                            os.path.join(os.getcwd(), "temp", f),
                            os.path.join(os.getcwd(), "download"),
                        )
                shutil.rmtree("./temp")
                os.makedirs("temp")
                self.log.info("下载发送任务结束，准备接受新任务")
                self.update_status("done")
            else:
                sleep(5)


xkw = Xkw()
while True:
    xkw.get_task()
