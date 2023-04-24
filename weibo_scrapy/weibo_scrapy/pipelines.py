# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql.cursors

class HotSearchScrapyPipeline():
    def __init__(self):
        # 连接数据库
        print("正在连接")
        self.connect = pymysql.connect(
            host='127.0.0.1',  # 数据库地址
            port=3306,  # 数据库端口
            db='whx',  # 数据库名
            user='root',  # 数据库用户名
            passwd='123',  # 数据库密码
            charset='utf8mb4',  # 编码方式
            )
            # 通过cursor执行增删查改
        print("连接成功")
        self.cursor = self.connect.cursor()
    def __del__(self):
        self.connect.close()
    def process_item(self, item, spider):
        sql = "replace into app01_hotsearch(raw_hot,word,category,ontime)value (%s,%s,%s,%s)"
        params = [item["raw_hot"],item["word"],item["category"],item["ontime"]]
        try:
            # self.cursor.executemany(sql, params)  # 执行sql语句
            self.cursor.execute(sql, params)  # 执行sql语句
            self.connect.commit()  # 执行事务
            # print("数据批量更新成功")
        except Exception as e:
            self.connect.rollback()
            # print("数据更新失败")
            print(e)
        return item  # 必须实现返回

class TextScrapyPipeline():
    def __init__(self):
        # 连接数据库
        print("正在连接")
        self.connect = pymysql.connect(
            host='127.0.0.1',  # 数据库地址
            port=3306,  # 数据库端口
            db='whx',  # 数据库名
            user='root',  # 数据库用户名
            passwd='123',  # 数据库密码
            charset='utf8mb4',  # 编码方式
            )
            # 通过cursor执行增删查改
        print("连接成功")
        self.cursor = self.connect.cursor()
    def __del__(self):
        self.connect.close()
    def process_item(self, item, spider):
        sql = "replace into app01_text(text_writer,text_time,text_url,text_content,text_forward_num,text_comment_num,text_like_num,text_word)value (%s,%s,%s,%s,%s,%s,%s,%s)"
        params = [item["text_writer"],item["text_time"],item["text_url"],item["text_content"],item["text_forward_num"],item["text_comment_num"],item["text_like_num"],item["text_word"]]
        try:
            # self.cursor.executemany(sql, params)  # 执行sql语句
            self.cursor.execute(sql, params)  # 执行sql语句
            self.connect.commit()  # 执行事务
            # print("文章数据更新成功")
        except Exception as e:
            self.connect.rollback()
            # print("文章数据更新失败")
            print(e)
        return item  # 必须实现返回

class CommentScrapyPipeline():
    def __init__(self):
        # 连接数据库
        print("正在连接")
        self.connect = pymysql.connect(
            host='127.0.0.1',  # 数据库地址
            port=3306,  # 数据库端口
            db='whx',  # 数据库名
            user='root',  # 数据库用户名
            passwd='123',  # 数据库密码
            charset='utf8mb4',  # 编码方式
            )
            # 通过cursor执行增删查改
        print("连接成功")
        self.cursor = self.connect.cursor()
    def __del__(self):
        self.connect.close()
    def process_item(self, item, spider):
        # total_num 为评论数
        sql = "replace into app01_comment(comment_writer,comment_time,comment_content,total_num,comment_like_num,comment_source,comment_text_url,text_word)value (%s,%s,%s,%s,%s,%s,%s,%s)"
        params = [item["comment_writer"],item["comment_time"],item["comment_content"],item["total_num"],item["comment_like_num"],item["comment_source"],item["comment_text_url"],item["text_word"]]
        try:
            # self.cursor.executemany(sql, params)  # 执行sql语句
            self.cursor.execute(sql, params)  # 执行sql语句
            self.connect.commit()  # 执行事务
            # print("评论数据更新成功")
        except Exception as e:
            self.connect.rollback()
            # print("评论数据更新失败")
            print(e)
        return item  # 必须实现返回