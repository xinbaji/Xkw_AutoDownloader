import json
import time
import os
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import Edge, EdgeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from utils.log import Log
import getpass
import platform

system = platform.system()

if system.startswith("Windows"):
    # USER_DIR_PATH = (f"C:/Users/{getpass.getuser()}/AppData/Local/Microsoft/Edge/User Data")
    USER_DIR_PATH = f"C:\\Users\\40751\\Desktop\\Xkw_AutoDownloader\\env"
    EXEC_DIR_PATH = f"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"


class Driver:

    def __init__(self, prefs: dict = {}) -> None:
        self.log = Log("selenium", "i")

        options = EdgeOptions()
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("detach", True)
        options.add_argument("--user-data-dir=" + USER_DIR_PATH)
        options.add_argument("--remote-debugging-port=9222")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("log-level=3")

        self.driver = Edge(options=options)
        self.driver.set_page_load_timeout(10)

    def get(self, url):
        self.driver.get(url)

    def wait_to_be(self, case, locator, retryTime: int = 12):
        """等待元素出现，返回网页元素对象

        Args:
            locator : union (By.selector,path)
            retryTime (int, optional): 重试次数. Defaults to 10.

        Returns:
            WebElement: 元素对象
        """
        argsDic = {
            "func_name": "appear_wait",
            "locator": locator,
            "retryTime": retryTime,
        }
        for i in range(0, retryTime, 1):
            try:
                self.log.debug("正在寻找元素：" + str(locator[1]))
                element = WebDriverWait(self.driver, 5).until(case(locator))
                return element
            except TimeoutException:
                self.log.debug("args:" + str(argsDic))
                self.log.error("第 " + str(i + 1) + " 次等待超时，刷新页面 ..")

                self.driver.refresh()

        self.log.error("等待元素超时" + str(argsDic))

    def wait_to_be_visible(self, locator, retryTime: int = 20) -> WebElement:
        return self.wait_to_be(EC.presence_of_element_located, locator, retryTime)

    def wait_to_be_clickable(self, locator, retryTime: int = 20) -> WebElement:
        return self.wait_to_be(EC.element_to_be_clickable, locator, retryTime)

    def wait_to_switch_iframe(self, locator, retryTime: int = 20) -> WebElement:
        return self.wait_to_be(
            EC.frame_to_be_available_and_switch_to_it, locator, retryTime=retryTime
        )

    def remove_elements(self, elements_list: list[str]):
        for i in elements_list:
            self.driver.execute_script("document.querySelector('" + i + "').remove()")

    def find_element(self, locator):
        return self.driver.find_element(locator[0], locator[1])

    def switch_to_last_window(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def close(self):
        self.driver.close()

    def refresh(self):
        self.driver.refresh()

    def get_page_source(self):
        return self.driver.page_source

    def switch_to_iframe(self, locator, retryTime: int = 10):
        """切换iframe

        Args:
            locator : union (By.selector,path)
            retryTime (int, optional): 重试次数. Defaults to 10.

        Returns:
            WebElement: 网页元素对象
        """
        argsDic = {
            "func_name": "switch_to_iframe",
            "locator": locator,
            "retryTime": retryTime,
        }
        for _ in range(0, retryTime, 1):
            try:
                element = WebDriverWait(self.driver, 60).until(
                    EC.frame_to_be_available_and_switch_to_it(locator)
                )
                return element
            except TimeoutException:
                self.log.error("切换iframe超时: args:" + str(argsDic))

    def switch_to_default_frame(self):
        try:
            self.driver.switch_to.default_content()
        except Exception as e:
            self.log.error("错误：" + str(e))

    def wait_string_to_be_visible(self, locator, string, retryTime: int = 15):
        """元素中出现目标文字，返回网页元素对象

        Args:
            locator : union (By.selector,path)
            retryTime (int, optional): 重试次数. Defaults to 15.

        Returns:
            WebElement: 网页元素对象
        """
        argsDic = {"func_name": "wait_string_to_be_visible", "locator": locator}
        for _ in range(0, retryTime, 1):
            try:
                elem = self.driver.find_element(*locator)
                self.log.debug(elem.text)
                if string in elem.text:
                    return elem
                else:

                    time.sleep(2)
            except NoSuchElementException:
                pass

        self.log.error("等待元素超时:" + str(argsDic))
        return False

    def force_click(self, locator):
        self.wait_to_be_visible(locator)
        elem = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].click()", elem)
