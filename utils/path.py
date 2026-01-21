from selenium.webdriver.common.by import By
from typing import Dict, Tuple


class Path:
    PATHS: Dict[str, str] = {
        "login_button": '/html/body/div[1]/div[1]/div/div/div[5]/span/a[1]',
        "login_status": '//*[@id="LoginInfo"]/span/a/span',
        "login_switch_button": "body > div.pop-window > div > div.xkw-login > div.scan-login.login-wrap > button",
        "login_username_input": '//*[@id="username"]',
        "login_password_input": '//*[@id="password"]',
        "login_commit_button": '//*[@id="accountLoginBtn"]',
        "ppt_download_button": '//*[@id="btnSoftDownload"]',
        "download_iframe": '//*[@id="layui-layer-iframe2"]',
        "download_confirm_button": "body > div > div.scan-code-content > a",
        "download_status": "/html/body/div[3]/div[2]/div[1]/div[1]/div/span", 
        "download_tip":'body > div:nth-child(5) > div.download-end.new-download-end.clearfix > div.download-end-left > div.download-item > div > div.tip-btn',
        "permission_deny_banner":'//*[@id="content"]/div/h2'
    }

    def __init__(self) -> None:
        pass

    def __getattr__(self, name):
        """动态获取定位器值"""
        if name in self.PATHS:
            def locator_method():
                return self.PATHS[name]
            return locator_method
        else:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

            
