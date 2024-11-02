from selenium.webdriver.common.by import By


class Url:
    def __init__(self) -> None:
        self.url = {}


class Xpath:

    def __init__(self) -> None:
        self.XPATH = {
            "login_status": '//*[@id="alreday-login"]/a/span',
            "login_button": '//*[@id="un-login"]/a[1]',
            "login_switch_button": "/html/body/div[1]/div/div[2]/div[4]/button",
            "login_username_input": '//*[@id="username"]',
            "login_password_input": '//*[@id="password"]',
            "login_commit_button": '//*[@id="accountLoginBtn"]',
            "ppt_download_button": '//*[@id="btnSoftDownload"]',
            "download_iframe": '//*[@id="layui-layer-iframe100002"]',
            "download_confirm_button": "/html/body/div[1]/div[2]/a",
            "download_status": "/html/body/div[3]/div[2]/div[1]/div[1]/div/span",
        }

    def login_status(self):
        locator = (By.XPATH, self.XPATH["login_status"])
        return locator

    def download_status(self):
        locator = (By.XPATH, self.XPATH["download_status"])
        return locator

    def login_button(self):
        locator = (By.XPATH, self.XPATH["login_button"])
        return locator

    def login_switch_button(self):
        locator = (By.XPATH, self.XPATH["login_switch_button"])
        return locator

    def login_username_input(self):
        locator = (By.XPATH, self.XPATH["login_username_input"])
        return locator

    def login_password_input(self):
        locator = (By.XPATH, self.XPATH["login_password_input"])
        return locator

    def login_commit_button(self):
        locator = (By.XPATH, self.XPATH["login_commit_button"])
        return locator

    def ppt_download_button(self):
        locator = (By.XPATH, self.XPATH["ppt_download_button"])
        return locator

    def download_iframe(self):
        locator = (By.XPATH, self.XPATH["download_iframe"])
        return locator

    def download_confirm_button(self):
        locator = (By.XPATH, self.XPATH["download_confirm_button"])
        return locator


class Css:
    def __init__(self) -> None:
        self.CSS = {
            "login_button": "#un-login > a.login-btn",
            "login_switch_button": "/html/body/div[1]/div/div[2]/div[4]/button",
            "login_username_input": '//*[@id="username"]',
            "login_password_input": '//*[@id="password"]',
            "login_commit_button": '//*[@id="accountLoginBtn"]',
            "ppt_download_button": '//*[@id="btnSoftDownload"]',
            "download_iframe": "/html/body/div[24]/div/iframe",
            "download_iframe2": "#layui-layer-iframe100002",
            "download_confirm_button": "/html/body/div[1]/div[2]/a",
        }

    def login_button(self):
        locator = (By.CSS_SELECTOR, self.CSS["login_button"])
        return locator

    def download_iframe2(self):
        locator = (By.CSS_SELECTOR, self.CSS["download_iframe2"])
        return locator
