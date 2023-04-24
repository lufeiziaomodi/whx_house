from multiprocessing import Process,Lock
from scrapy import cmdline
import time
import logging
lock = Lock()
# 创建爬虫进程
def start_spider(spider_name, frequency):
    lock.acquire()
    args = spider_name.split()
    print("进程开始")
    start = time.time()
    p = Process(target=cmdline.execute, args=(args,))
    p.start()
    p.join()
    lock.release()
    logging.debug("### use time: %s" % (time.time() - start))
    time.sleep(frequency)
    print("进程结束")
#删除热搜
def del_hotsearch():
    import pymysql
    print("正在连接")
    connect = pymysql.connect(
        host='127.0.0.1',  # 数据库地址
        port=3306,  # 数据库端口
        db='whx',  # 数据库名
        user='root',  # 数据库用户名
        passwd='123',  # 数据库密码
        charset='utf8mb4',  # 编码方式
    )
    # 通过cursor执行增删查改
    print("连接成功")
    cursor = connect.cursor()
    sql = " delete from app01_hotsearch"
    cursor.execute(sql)
    print("删除热搜表")
    connect.commit()  # 执行事务
    connect.close()
# 连接并删除文章和评论
def con(confs,sog):
    import pymysql
    print("正在连接")
    connect = pymysql.connect(
        host='127.0.0.1',  # 数据库地址
        port=3306,  # 数据库端口
        db='whx',  # 数据库名
        user='root',  # 数据库用户名
        passwd='123',  # 数据库密码
        charset='utf8mb4',  # 编码方式
    )
    # 通过cursor执行增删查改
    print("连接成功")
    cursor = connect.cursor()
    sql = "select word from app01_hotsearch order by raw_hot desc"
    word_list = []
    # 搜索页数修改
    cmd_str = "scrapy crawl hotsearch_text -a word={} -a page=50"
    try:
        # self.cursor.executemany(sql, params)  # 执行sql语句
        cursor.execute(sql)  # 执行sql语句
        hot_search_list = list(cursor.fetchall())
        num =0
        for hot_search in hot_search_list:
            if num <sog:
                d = {}
                d["spider_name"] = cmd_str.format("#" + hot_search[0].replace(" ", "") + "#")
                d["frequency"] = 1
                confs.append(d)
            else:
                break
            num =num +1
        connect.commit()  # 执行事务
        print("数据提取更新成功")
    except Exception as e:
        connect.rollback()
        print("数据提取失败")
        print(e)
    sql = " delete from app01_text"
    cursor.execute(sql)
    print("删除文章表")
    sql = " delete from app01_comment"
    cursor.execute(sql)
    print("删除评论表")
    connect.commit()  # 执行事务
    connect.close()
# # 保存评论至csv文件
def csv_save():
    import pymysql
    print("正在连接")
    connect = pymysql.connect(
        host='127.0.0.1',  # 数据库地址
        port=3306,  # 数据库端口
        db='whx',  # 数据库名
        user='root',  # 数据库用户名
        passwd='123',  # 数据库密码
        charset='utf8mb4',  # 编码方式
    )
    # 通过cursor执行增删查改
    print("连接成功")
    cursor = connect.cursor()
    sql = "select word from app01_hotsearch order by raw_hot desc"
    word_list = []
    try:
        # self.cursor.executemany(sql, params)  # 执行sql语句
        cursor.execute(sql)  # 执行sql语句
        hot_search_list = list(cursor.fetchall())
        num = 0
        for hot_search in hot_search_list:
            if num < 5:
                word_list.append(hot_search[0])
            else:
                break
            num = num + 1
        connect.commit()  # 执行事务
        print("数据提取更新成功")
    except Exception as e:
        connect.rollback()
        print("数据提取失败")
        print(e)
    # print(word_list)
    comment_list = []
    import csv
    num = 0
    csv_name = "{}.csv"
    path = "../app01/static/form/"
    for word in word_list:
        num = num + 1
        sql = "select comment_content from app01_comment where text_word = '#{}#'".format(word)
        cursor.execute(sql)
        comment_list = list(cursor.fetchall())
        with open(path + csv_name.format(num), 'w', newline='', encoding='utf8') as f:
            writer = csv.writer(f)
            writer.writerows(comment_list)
    # 修改最近最晚时间
    sql = "select comment_time from app01_comment order by comment_time desc"
    cursor.execute(sql)
    new = list(cursor.fetchall())[0][0]
    # print(new)
    sql = "select comment_time from app01_comment order by comment_time asc"
    cursor.execute(sql)
    old= list(cursor.fetchall())[0][0]
    sql = "delete from app01_spidertime"
    cursor.execute(sql)
    connect.commit()
    # print("删除成功")
    print(new,old)
    sql ="replace into app01_spidertime(new,old)value (%s,%s)"
    params = [new,old]
    cursor.execute(sql,params)
    connect.commit()

if __name__ == '__main__':
    # 配置参数即可, 爬虫名称，运行频率
    # 先爬热搜
    # 删除热搜表
    del_hotsearch()
    d = {}
    d["spider_name"] = "scrapy crawl hotsearch"
    d["frequency"] = 1
    print(d["spider_name"], d["frequency"])
    process = Process(target=start_spider,
                    args=(d["spider_name"], d["frequency"]))
    process.start()
    process.join()
    confs = []
    # 取话题前pos个
    con(confs,5)
    # for i in confs:
    #     print(i)
    for conf in confs:
        print(conf["spider_name"], conf["frequency"])
        process = Process(target=start_spider,
                          args=(conf["spider_name"], conf["frequency"]))
        process.start()
    process.join()
    # 评论
    d = {}
    d["spider_name"] = "scrapy crawl comment"
    d["frequency"] = 1
    process = Process(target=start_spider,
                      args=(d["spider_name"], d["frequency"]))
    process.start()
    process.join()
    csv_save()





