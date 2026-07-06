# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from itemadapter import ItemAdapter
import match from scripts.s_login import match


class LoginSpiderMiddleware:
    def __init__(self):
        self.authorization = None
    def get_authorization(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        service = Service(executable_path="chromedriver.exe")
        # 创建浏览器实例
        dirver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            dreiver.get("https://pro.crmeb.net/admin/login")
            time.sleep(3)
            # print("driver.title", driver.title)
            # search_box = driver.find_element(By.XPATH, '//*[@id="user_login"]')
            # search_box.clear()
            # search_box.send_keys("demo")
            # search_box = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/form[1]/div[2]/div/div/input')
            # search_box.clear()
            # search_box.send_keys("crmeb.com")
            search_box = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/form[1]/div[3]/div/button')
            search_box.click()
        except Exception as e:
            print("error", e)
        finally:
            self.authorization = driver.get_cookies()   
            print("driver.quit")
            driver.quit()
    def process_request(self, request, spider):
        if self.authorization is None:
            self.authorization = self.get_authorization()
            request.headers["authori-zation"] = f"Bearer {authorization[3]['value']}"


if __name__ == "__main__":
    login_spider_middleware = LoginSpiderMiddleware()
    login_spider_middleware.get_authorization()
