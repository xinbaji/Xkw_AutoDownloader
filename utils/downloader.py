import os
from utils.log import Log
from utils.path import Path
from utils.controller import Driver
from setting import Setting
class Downloader:
    def __init__(self) -> None:
        self.path = Path()
        if Setting.download_location != "":
            self.download_location = Setting.download_location
        else:
            self.download_location = os.path.join(os.getcwd(), "download")
        
        self.log = Log("downloader", "d").logger
        self.driver = Driver()
        self.username = Setting.username
        self.password = Setting.password
        
        
    
    def handle_login_button(self):
        self.log.info("未登录，正在登录... (过程中可能会出现微信验证与验证码需手动操作)")
        self.driver.wait("visible", self.path.login_button()).click()
        self.driver.implicitly_wait(60)
        self.driver.wait("visible", self.path.login_switch_button()).click()
        self.driver.wait("visible", self.path.login_username_input()).send_keys(
            self.username
        )
        self.driver.wait("visible", self.path.login_password_input()).send_keys(
            self.password
        )
        self.driver.wait("visible", self.path.login_commit_button()).click()
        
        self.driver.implicitly_wait(60)
            
       
    
    def handle_already_login(self):
        self.driver.implicitly_wait(60)
   
    def login(self):
        self.driver.wait("visible", self.path.login_button(),timeout=5,no_exception=True).do(self.handle_login_button)
        self.driver.wait("visible", self.path.login_status(),timeout=5).do(self.handle_already_login)
        
    
    def handle_download_iframe(self):
        self.driver.wait("visible", self.path.download_iframe()).switch()
        self.driver.implicitly_wait(60)
        self.driver.wait("visible", self.path.download_confirm_button()).click()
        self.driver.implicitly_wait(60)
        self.driver.switch_to_default_frame()
    
    def handle_no_iframe(self):
        pass
    def download(self, url: str) -> bool:
        self.driver.get(url)
        self.driver.implicitly_wait(60)
        self.login()
        self.driver.wait("visible", self.path.ppt_download_button()).click()
        self.driver.implicitly_wait(60)
        self.driver.wait("visible", self.path.download_status(),timeout=5).do(self.handle_download_iframe)
        self.driver.implicitly_wait(60)
        self.driver.wait("visible", self.path.download_tip(),timeout=10).do(self.handle_no_iframe)
        
        self.log.info("正在下载, 地址: "+url)
        
        

        
