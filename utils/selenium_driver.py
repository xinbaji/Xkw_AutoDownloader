import json
import time
import os
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import Edge, EdgeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from utils.log import Log


class Driver:

    def __init__(self, prefs: dict = {}) -> None:
        self.log = Log("selenium", "i")

        options = EdgeOptions()
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("detach", True)
        self.driver = Edge(options=options)
        self.driver.set_page_load_timeout(10)

    def wait_to_be(self, case, locator, retryTime: int = 12):
        """等待元素出现或元素中出现目标文字，返回网页元素对象

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

    def wait_to_be_visible(self, locator, retryTime: int = 12) -> WebElement:
        return self.wait_to_be(EC.presence_of_element_located, locator, retryTime)

    def wait_to_be_clickable(self, locator, retryTime: int = 12) -> WebElement:
        return self.wait_to_be(EC.element_to_be_clickable, locator, retryTime)

    def wait_to_switch_iframe(self, locator, retryTime: int = 12) -> WebElement:
        return self.wait_to_be(
            EC.frame_to_be_available_and_switch_to_it, locator, retryTime=retryTime
        )

    def get(self, url, cookies: bool = False):
        try:
            self.driver.get(url)
            if cookies and os.path.exists("./data/cookies.json"):
                with open("./data/cookies.json", "r") as f:
                    cookies = json.load(f)
                    f.close()
                for i in cookies:
                    self.driver.add_cookie(i)
                self.driver.refresh()

        except TimeoutException:
            pass

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
        """等待元素出现或元素中出现目标文字，返回网页元素对象

        Args:
            locator : union (By.selector,path)
            retryTime (int, optional): 重试次数. Defaults to 10.

        Returns:
            WebElement: 元素对象
        """
        argsDic = {
            "func_name": "switch_to_iframe",
            "locator": locator,
            "retryTime": retryTime,
        }
        for i in range(0, retryTime, 1):
            try:
                element = WebDriverWait(self.driver, 60).until(
                    EC.frame_to_be_available_and_switch_to_it(locator)
                )
                return element
            except TimeoutException:
                self.log.debug("args:" + str(argsDic))
                self.log.error("第 " + str(i + 1) + " 次等待超时，刷新页面 ..")

                self.driver.refresh()

    def switch_to_default_frame(self):
        self.driver.switch_to.default_content()

    def wait_string_to_be_visible(self, locator, string, retryTime: int = 15):
        """元素中出现目标文字，返回网页元素对象

        Args:
            locator : union (By.selector,path)
            retryTime (int, optional): 重试次数. Defaults to 15.

        Returns:
            WebElement: 元素对象
        """
        argsDic = {
            "func_name": "wait_string_to_be_visible",
            "locator": locator,
            "retryTime": retryTime,
        }
        for i in range(0, retryTime, 1):
            try:
                elem = self.driver.find_element(*locator)
                self.log.debug(elem.text)
                if string in elem.text:
                    return elem
                else:

                    time.sleep(2)
            except NoSuchElementException:
                pass

        self.log.error("等待元素超时" + str(argsDic))
        return False

    def save_cookies(self):
        cookies = self.driver.get_cookies()
        """#TODO cookies 清洗
        for i in cookies:
            del i['domain']
            del i['httpOnly']
            del i['path']
            del i['sameSite']
            del i['secure']"""

        with open("./data/cookies.json", "w") as f:
            f.write(json.dumps(cookies))
            f.close()
        self.log.debug("cookies.json 保存成功!")

    def force_click(self, locator):
        self.wait_to_be_visible(locator)
        elem = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].click()", elem)
