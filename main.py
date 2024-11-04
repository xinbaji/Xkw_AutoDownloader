import os
import json
import shutil
import yagmail

from time import sleep
from threading import Thread
from smtplib import SMTPSenderRefused

from utils.log import Log
from utils.encrypt import pwdcfiiro1c, usnmdcfiiro1cqqt
from utils.selenium_driver import Driver
from data.path import Xpath, Css
from config.config import Config
from utils.selenium_driver import TimeoutException


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
        # 清空临时文件夹
        shutil.rmtree("./temp")
        os.makedirs("temp")

        self.xpath = Xpath()
        self.css = Css()
        self.log = Log("main", "d")

    def login(self):

        self.driver.wait_to_be_visible(self.css.login_button()).click()
        self.driver.wait_to_be_visible(self.xpath.login_switch_button())
        sleep(5)
        self.driver.wait_to_be_visible(self.xpath.login_switch_button()).click()
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

    def purchase_iframe_handler(self) -> None:
        # 处理点击下载按钮后的网校通付费弹窗
        try:
            self.driver.switch_to_iframe(self.css.download_iframe2())
        except TimeoutException as te:
            self.log.info("此文件下载过或遇到未知情况，直接下载")
        else:
            self.driver.wait_to_be_clickable(self.xpath.download_confirm_button())
            sleep(5)
            self.driver.wait_to_be_clickable(
                self.xpath.download_confirm_button()
            ).click()

    def download(self, url):

        self.driver.get(url)
        self.driver.driver.implicitly_wait(60)
        if os.path.exists(".\\env\\Login_ok.txt") == False:
            self.login()
        self.driver.wait_to_be_visible(self.xpath.ppt_download_button())
        sleep(1)
        self.driver.force_click(self.xpath.ppt_download_button())
        sleep(3)

        thread1 = Thread(target=self.wait_crdownload_appear)
        thread1.start()
        thread2 = Thread(target=self.purchase_iframe_handler)
        thread2.start()
        thread1.join()
        self.driver.get("https://www.zxxk.com/")

    def wait_crdownload_appear(self, retryTime: int = 120) -> bool:
        # TODO:添加对文件名的检测，目前上一个文件未下载完成时下一个文件直接判定为已创建下载任务
        # TODO :标题匹配， + 空格删掉
        for _ in range(0, retryTime * 2, 1):
            filelist = os.listdir(".\\temp")
            if len(filelist) != 0:
                for i in range(0, len(filelist), 1):
                    if "cr" in filelist[i]:
                        self.log.info("下载任务已创建")
                        return True
            else:
                pass
            sleep(0.5)

        raise TimeoutError

    def wait_crdownload_disappear(self) -> None:
        while True:
            filelist = os.listdir(".\\temp")
            if len(filelist) != 0:
                for i in range(0, len(filelist), 1):
                    if "cr" in filelist[i]:
                        self.log.info("下载未完成")
                        sleep(5)
                        break
                self.log.info("文件已经全部下载完成...")
                break

    def send_yagmail(self, recipientAddrs):
        host_domain_list = ["163.com", "qq.com"]
        for i in host_domain_list:
            if i in self.config.send_from_email():
                host_domain = "smtp." + i
        yag_server = yagmail.SMTP(
            user=self.config.send_from_email(),
            password=self.config.code(),
            host=host_domain,
        )
        email_to = [
            recipientAddrs,
        ]
        email_attachment_list = []
        for i in os.listdir(".\\temp"):
            email_attachment_list.append(os.path.join(".\\temp", i))
        email_title = (
            email_attachment_list[0].replace(".\\temp\\", "") + "等文件 (自动发送）"
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

        self.driver = Driver()
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
                self.wait_crdownload_disappear()
                sleep(1)
                if task["recv_email"] != "":
                    try:
                        self.send_yagmail(task["recv_email"])

                    except SMTPSenderRefused as sr:
                        self.log.error("Message too large.")

                else:
                    for f in os.listdir(".\\temp"):
                        # TODO：移动文件有点问题
                        try:
                            shutil.move(
                                os.path.join(os.getcwd(), "temp", f),
                                os.path.join(os.getcwd(), "download"),
                            )
                        except shutil.Error as e:
                            if "already exists" in e:
                                pass
                            else:
                                self.log.error(e)
                                raise shutil.Error(e)
                self.log.info("任务完成，准备清理临时文件...")
                while True:
                    try:
                        shutil.rmtree("./temp")
                        break
                    except PermissionError as e:
                        self.log.debug(e)
                        if "另一个程序正在使用" in e:
                            sleep(5)
                os.makedirs("temp")
                self.log.info("下载发送任务结束，准备接受新任务")
                self.update_status("done")
            else:
                sleep(5)


xkw = Xkw()
while True:
    xkw.get_task()
