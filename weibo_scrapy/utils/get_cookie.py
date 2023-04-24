
import json
import time

# 项目导入
from WeiBo_demo import WeiBoDemo


if __name__ == '__main__':
    # 获取cookie
    wb = WeiBoDemo()
    wb.open_weibo()
    wb.login_mail()
    with open('weibo.json', 'w') as f:
        json.dump(wb.browser.get_cookies(), f)
    print("save is ok")
    time.sleep(100)

    # # 模拟登录
    # wb = WeiBo()
    # wb.open_weibo()
    # add_cookies(wb.browser, 'weibo.json')
    # wb.open_weibo()
    # time.sleep(100)

