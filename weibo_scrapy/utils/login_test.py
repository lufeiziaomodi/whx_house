import time

# 项目导入
from WeiBo_demo import WeiBoDemo

if __name__ == '__main__':
    # 模拟登录
    wb = WeiBoDemo()
    wb.open_weibo()
    wb.add_cookies()
    wb.open_weibo()
    time.sleep(100)