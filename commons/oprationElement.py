from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
#from base.get_logger import GetLogger
# import page
from selenium.webdriver.chrome.options import Options

# 获取log日志器
#log = GetLogger().get_logger()


class WebDriverWrapper:
    def __init__(self, driver_path):

        options = Options()
        # 隐藏自动化特征，百度有识别自动化。。
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        self.driver = webdriver.Chrome(options=options,service=Service(driver_path))
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })


        # self.driver = webdriver.Chrome(service=Service(driver_path))
        self.driver.maximize_window()



    def find_element(self, by, value):
        try:
            # print(f'by={by}')
            # print(f'value={value}')
            return self.driver.find_element(by, value)
        except NoSuchElementException:
            print(f"Element not found with {by}={value}")
            return None

    def click_element(self, by, value):
        x = 0  # 默认成功，1为失败
        element = self.find_element(by, value)
        if element:
            element.click()
        else:
            x=1
            print("Element not found to click.")
        return x

    def input_text(self, by, value, text):
        x=0#默认成功，1为失败
        element = self.find_element(by, value)
        if element:
            element.clear()  # Clear existing text if any
            element.send_keys(text)
        else:
            x=1
            print("Element not found to input text.")
        return x

    def get_element_text(self, by, value):
        element = self.find_element(by, value)
        if element:
            return element.text
        else:
            print("Element not found to get text.")
            return ""

    # 截图 方法封装
    def base_get_image(self):
        #log.info("[base]: 断言出错，调用截图")
        self.driver.get_screenshot_as_file("./image/{}.png".format(time.strftime("%Y_%m_%d %H_%M_%S")))


    # 判断元素是否存在 方法封装
    def base_element_is_exist(self, by,value):
        try:
            self.find_element(by,value, timeout=5)
            #log.info("[base]: {} 元素查找成功，存在页面".format(loc))
            return True  # 代表元素存在
        except Exception as e:
            #log.error("[base]：发生错误{}，{} 元素查找失败，不存在当前页面".format(e, loc))
            return False  # 代表元素不存在

    # 回到首(页购物车、下订单、支付)都需要用到此方法
    def base_index(self):
        time.sleep(5)
        self.driver.get(page.URL)

    # 切换frame表单方法
    def base_switch_frame(self, name):
        self.driver.switch_to.frame(name)

    # 回到默认目录方法
    def base_default_content(self):
        self.driver.switch_to.default_content()

    # 切换窗口 方法 调用此方法
    def base_switch_to_window(self, title):
        log.info("正在执行切换title值为：{}窗口 ".format(title))
        self.driver.switch_to.window(self.base_get_title_handle(title))

    # 获取指定title页面的handle方法
    def base_get_title_handle(self, title):
        # 获取当前页面所有的handles
        for handle in self.driver.window_handles:
            log.info("正在遍历handles：{}-->{}".format(handle, self.driver.window_handles))
            # 切换 handle
            self.driver.switch_to.window(handle)
            log.info("切换 :{} 窗口".format(handle))
            # 获取当前页面title 并判断 是否等于 指定参数title
            log.info("判断当前页面title:{} 是否等于指定的title:{}".format(self.driver.title, title))
            if self.driver.title == title:
                log.info("条件成立！ 返回当前handle{}".format(handle))
                # 返回 handle
                return handle


    def close(self):
        self.driver.quit()

    def get(self, url):
        self.driver.get(url)

    def title(self):
        return self.driver.title

