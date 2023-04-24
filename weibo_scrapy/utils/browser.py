import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def create_chrome_driver(*, headless=False):  # 创建谷歌浏览器对象，用selenium控制浏览器访问url
    driver_path = 'chromedriver.exe'
    service = Service(driver_path)
    options = webdriver.ChromeOptions()
    if headless:  # 如果为True，则爬取时不显示浏览器窗口
        options.add_argument('--headless')
    options.add_argument('-ignore-certificate-errors')
    options.add_argument('-ignore -ssl-errors')
    # 做一些控制上的优化
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    # 创建浏览器对象
    browser = webdriver.Chrome(options=options,service=service)
    # 破解反爬措施
    browser.execute_cdp_cmd(
        'Page.addScriptToEvaluateOnNewDocument',
        {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'}
    )
    return browser

def get_cookie(cookie_file):
    cookie=[]
    with open(cookie_file, 'r') as file:
        cookies_list = json.load(file)
        for key in cookies_list:
            if key['secure']:
                # print(key)
                cookie.append(key)
    return cookie

def add_cookies(browser,cookie_file):
    # browser.add_cookie(get_cookie('weibo.json'))
    with open(cookie_file,'r') as file:
        cookies_list = json.load(file)
        for key in cookies_list:
            if key['secure']:
                browser.add_cookie(key)

# print(get_cookie('weibo.json'))
# wb=create_chrome_driver(headless=False)
# wb.get("https://weibo.com/")
# add_cookies(wb,'weibo.json')
# wb.get("https://weibo.com/")
# print(wb.page_source)
# time.sleep(100)
# wb.close()
