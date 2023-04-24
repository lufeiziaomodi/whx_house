from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os
import json
import time

# 项目导入
from utils.browser import add_cookies, create_chrome_driver
# from login import add_cookies, create_chrome_driver


class WeiBo():
    # 1.模拟访问网址
    url = "https://weibo.com/"
    # True 不显示模拟浏览器页面
    browser = create_chrome_driver(headless=True)

    def open_weibo(self):  # 打开微博
        self.browser.maximize_window()  # 需要全屏后才能显示那个登录框
        self.browser.get(self.url)  # 访问微博官网
        time.sleep(1)

    def login_mail(self):  # 短信登录
        self.browser.get(
            self.url.join('newlogin?tabtype=weibo&gid=102803&openLoginLayer=0&url=https%3A%2F%2Fweibo.com%2F'))
        time.sleep(4)
        self.browser.find_element(by=By.XPATH,
                                  value='/html/body/div/div[2]/div[2]/div[2]/main/div[2]/div/div/div[2]/div[1]/div/button').click()  # 点击短信登录按钮
        wait_obj = WebDriverWait(self.browser, 20)
        wait_obj.until(expected_conditions.presence_of_all_elements_located(
            (By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[1]/a[5]')))
        # self.save_cookie()
        # print('save is ok')
        # time.sleep(1000)

    # def save_cookie(self):
    #     print(self.browser.get_cookies())
    #     with open('weibo.json', 'w') as f:
    #         json.dump(self.browser.get_cookies(), f)

    def save_cookie(self):
        print(self.browser.get_cookies())
        with open('utils/weibo.json', 'w') as f:
            json.dump(self.browser.get_cookies(), f)

    # def __del__(self):
    #     self.browser.close()
    #     self.browser.quit()

    # def add_cookies(self):
    #     add_cookies(self.browser, 'weibo.json')

    # 项目导入
    def add_cookies(self):
        add_cookies(self.browser, 'utils/weibo.json')

if __name__ == '__main__':
    # 获取cookie
    # wb = WeiBo()
    # wb.open_weibo()
    # wb.login_mail()
    # with open('weibo.json', 'w') as f:
    #     json.dump(wb.browser.get_cookies(), f)
    # print("save is ok")
    # time.sleep(100)

    # 模拟登录
    wb = WeiBo()
    wb.open_weibo()
    add_cookies(wb.browser, 'weibo.json')
    wb.open_weibo()
    time.sleep(100)

