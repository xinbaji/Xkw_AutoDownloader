import json
import time
import os
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
)

from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from utils.log import Log
from config.config import Config

class NoSuchDriverException(Exception):
    pass

class Driver:

    def __init__(self) -> None:
        self.config = Config()
        self.log = Log("selenium", "i")

        if self.config.default_driver() == "chrome":
            __driver = Chrome
            options = ChromeOptions()
        elif self.config.default_driver() == "edge":
            __driver = Edge
            options = EdgeOptions()
        else:
            if self.driver_isavailable(target_driver=Chrome):
                __driver = Chrome
                options = ChromeOptions()
                self.config.add("driver", "chrome")
            elif self.driver_isavailable(target_driver=Edge):
                __driver = Edge
                options = EdgeOptions()
                self.config.add("driver", "edge")
            else:
                self.log.error("无支持的浏览器，安装edge或chrome。")
                raise NoSuchDriverException("无支持的浏览器，安装edge或chrome。")
        self.download_location = os.path.join(os.getcwd(), "temp")
        self.prefs = {"download.default_directory": self.download_location}
        self.USER_DIR_PATH = os.path.join(os.getcwd(), "env")
        options.add_experimental_option("prefs", self.prefs)
        options.add_experimental_option("detach", True)
        options.add_argument("--user-data-dir=" + self.USER_DIR_PATH)
        options.add_argument("--remote-debugging-port=9222")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("log-level=3")
        self.driver = __driver(options=options)
        self.driver.set_page_load_timeout(10)

    def driver_isavailable(self, target_driver) -> bool:
        try:
            __driver = target_driver()
        except NoSuchDriverException:
            return False
        except Exception as e:
            self.log.error(e)
            return False
        else:
            return True

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
        try:
            self.log.info(
                "正在寻找元素：" + str(locator[1]) + "寻找成功条件：" + str(case)
            )
            element = WebDriverWait(self.driver, retryTime).until(case(locator))
            return element
        except TimeoutException:
            self.log.debug("args:" + str(argsDic))
            self.log.error("等待元素超时" + str(argsDic))
            raise TimeoutException

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
        try:
            element = WebDriverWait(self.driver, retryTime).until(
                EC.frame_to_be_available_and_switch_to_it(locator)
            )
            return element
        except TimeoutException:
            pass
        self.log.error("切换iframe超时: args:" + str(argsDic))
        raise TimeoutException

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
