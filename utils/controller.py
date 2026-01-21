from utils.log import Log
import os
import time
from functools import wraps
from threading import Thread
from datetime import datetime
from selenium.common import ScreenshotException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By,ByType
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from typing import overload
from setting import Setting

class BaseEasySeleniumException(Exception):
    def __init__(self, msg):
        self.msg = msg
        Log("Error").logger.error(msg)

    def __str__(self):
        return self.msg


class NoSuchDriverException(BaseEasySeleniumException): ...


class PathInvalid(BaseEasySeleniumException): ...


class NoSuchCaseException(BaseEasySeleniumException): ...


class NoSuchElementException(BaseEasySeleniumException): ...
def timeout_setter(timeout_seconds):
    """
    装饰器：开启一个线程执行被装饰的函数，并计时，超过指定时间则终止执行
    
    Args:
        timeout_seconds (float): 超时时间（秒）
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = [None]  # 使用列表存储结果，以便在线程中修改
            exception = [None]  # 存储异常对象

            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e

            thread = Thread(target=target)
            thread.daemon = True  # 设置为守护线程
            thread.start()
            thread.join(timeout_seconds)  # 等待指定时间

            if thread.is_alive():  # 如果线程仍在运行，说明超时了
                print(f"Function {func.__name__} timed out after {timeout_seconds} seconds")
                
                raise TimeoutException(f"Function {func.__name__} timed out after {timeout_seconds} seconds")# 或者抛出异常，根据需求决定
            elif exception[0]:  # 如果函数执行过程中出现异常
                raise exception[0]
            else:  # 正常完成
                return result[0]

        return wrapper
    return decorator

def only_chained_calls(func):
    def wrapper(self, *args, **kwargs):
        if self.temp_element is not None:
            result = func(self, *args, **kwargs)
            self.temp_element = None
            self.temp_locator = None
            return result
        else:
            raise NoSuchElementException("被处理的元素不存在")

    return wrapper


class Driver:
    case_dict ={
            "visible": EC.presence_of_element_located,
            "clickable": EC.element_to_be_clickable,
            "iframe_available": EC.frame_to_be_available_and_switch_to_it,
            "string_visible": EC.text_to_be_present_in_element,
        }
    def __init__(self) -> None:

        self.log = Log("Controller", "d").logger
        if not os.path.exists("env"):
            os.makedirs("env")
        if os.path.exists("env/browser.txt"):
            with open("env/browser.txt", "r") as f:
                driver_str = f.read()
                if driver_str not in ["chrome", "edge"]:
                    driver_str = self._driver_isavailable()
        else:
            driver_str = self._driver_isavailable()

        if "chrome" in driver_str:
            __driver = Chrome
            options = ChromeOptions()
            self.log.debug("当前浏览器: Chrome")
        elif "edge" in driver_str:
            __driver = Edge
            options = EdgeOptions()
            self.log.debug("当前浏览器: Edge")
        else:
            raise NoSuchDriverException("无支持的浏览器，安装Edge或Chrome。")

          
        if len(Setting.download_location) > 3:
            self.download_location = Setting.download_location
        else:
            if not os.path.exists("download"):
                os.makedirs("download")
            self.download_location = os.path.join(os.getcwd(), "download")
        self.prefs = {"download.default_directory": self.download_location}

        self.userdata_dir = os.path.join(os.getcwd(), "env")

        
        self.timeout_seconds = 12

        self.temp_element: WebElement = None
        self.temp_locator: tuple = None

        options.add_experimental_option("prefs", self.prefs)
        options.add_experimental_option("detach", True)
        options.add_argument("--user-data-dir=" + self.userdata_dir)
        options.add_argument("--remote-debugging-port=9222")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("log-level=3")
        self.driver = __driver(options=options)
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(self.timeout_seconds)
        

    def _driver_isavailable(self) -> str:
        driver_dict = {"chrome": Chrome, "edge": Edge}
        for driver_str, driver_class in driver_dict.items():
            try:
                driver = driver_class()
            except Exception as e:
                self.log.error(e)
            else:
                driver.quit()
                with open("./env/browser.txt", "w") as f:
                    f.write(driver_str)
                return driver_str

        raise NoSuchDriverException("无支持的浏览器，安装Edge或Chrome。")

    def get(self, url):
        self.driver.get(url)
   
   
    def path_to_locator(self, path: str) -> tuple:
        if "/" == path[0]:
            return (By.XPATH, path)
        else:
            return (By.CSS_SELECTOR, path)

    def wait(self, case: str, path: str, target_string="", timeout=-1,no_exception=False):
        
        
        if timeout < 0:
            timeout = self.timeout_seconds
        if case not in self.case_dict.keys():
            raise NoSuchCaseException(
                "case错误, 可用case列表: " + str(self.case_dict.keys())
            )
        
        locator = self.path_to_locator(path)

        for key, value in self.case_dict.items():
            if case == key:
                case_handler = value
                case_handler_value =  locator
                break

        if case_handler == EC.text_to_be_present_in_element:
            case_handler_value = (locator, target_string)

        self.driver.implicitly_wait(timeout)

        self.log.info(
            "正在寻找元素: "
            + str (locator)
            + " 寻找成功条件: "
            + str(case)
            + " 等待时间(秒): "
            + str(timeout)
        )
        try:
            element = WebDriverWait(self.driver, timeout).until(
                case_handler(case_handler_value)
            )
        except TimeoutException as e:
            if no_exception:  # 如果不需要异常
                return self
            self.log.error("等待元素超时")
            raise e
        else:
            self.temp_element = element
            self.temp_locator = locator
        return self

    @only_chained_calls
    def remove(self):
        self.driver.execute_script(
            "document.querySelector('" + self.temp_element + "').remove()"
        )

    @only_chained_calls
    def click(self):
        self.temp_element.click()

    @only_chained_calls
    def send_keys(self, keys):
        self.temp_element.send_keys(keys)

    @only_chained_calls
    def get_attribute(self, attr):
        return self.temp_element.get_attribute(attr)

    @only_chained_calls
    def get_text(self):
        return self.temp_element.text

    @only_chained_calls
    def force_click(self):
        self.driver.execute_script("arguments[0].click()", self.temp_element)

    @only_chained_calls
    def clear(self):
        self.temp_element.clear()

    def screenshot(self):
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots", exist_ok=True)
        filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")[:-4] + ".png"
        filepath = os.path.join(os.getcwd(), "screenshots", filename).replace("\\", "/")
        self.log.debug("element: " + str(self.temp_element))
        self.log.debug("save_path: " + filepath)
        result = self.temp_element.screenshot(filepath)
        if not result:
            raise ScreenshotException("截图写入文件失败，请检查该工作目录的读写权限")

    def switch_to_last_window(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def close(self):
        self.driver.close()

    def refresh(self):
        self.driver.refresh()

    def get_page_source(self):
        return self.driver.page_source

    def implicitly_wait(self, seconds):
        return self.driver.implicitly_wait(seconds)

    def sleep(self,seconds):
        return time.sleep(seconds)
    def switch_to_default_frame(self):
        try:
            self.driver.switch_to.default_content()
        except Exception as e:
            self.log.error("错误：" + str(e))
    @only_chained_calls
    def switch(self):
        self.driver.switch_to.frame(self.temp_element)
    @only_chained_calls
    def do(self,handler):
        handler()


