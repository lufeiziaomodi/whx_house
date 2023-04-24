from scrapy.spiders import Spider
from scrapy import Request,Selector
import json
import argparse
import datetime
from urllib import parse
import pymysql
from weibo_scrapy.items import CommentItem


class CommentSpider(Spider):
    def __init__(self):
        # 连接数据库
        print("正在连接")
        self.connect = pymysql.connect(
            host='127.0.0.1',  # 数据库地址
            port=3306,  # 数据库端口
            db='whx',  # 数据库名
            user='root',  # 数据库用户名
            passwd='123',  # 数据库密码
            charset='utf8',  # 编码方式
            )
            # 通过cursor执行增删查改
        print("连接成功")
        self.cursor = self.connect.cursor()
        # 其他设置
        sql = "select text_url,text_word,text_comment_num from app01_text"
        try:
            # self.cursor.executemany(sql, params)  # 执行sql语句
            self.cursor.execute(sql)  # 执行sql语句
            self.url_sign=[]
            self.url_list=[]
            self.url = []  # 执行sql语句
            self.word=[]
            # 模板
            url_sign1 = 'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={}&is_show_bulletin=2&is_mix=0&count=10&uid={}&fetch_level=0'
            # 按时间排序
            # url_sign1 = 'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={}&flow=1&is_show_bulletin=2&is_mix=0&count=10&uid={}&fetch_level=0'
            url_sign2 = 'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={}&flow=0&is_show_bulletin=2&is_mix=0&count=20&uid={}&fetch_level=0'
            # 按时间排序
            # url_sign2 = 'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={}&flow=1&is_show_bulletin=2&is_mix=0&count=20&uid={}&fetch_level=0'
            uid=0
            id=0
            url=""
            url_list = list(self.cursor.fetchall())  # 执行sql语句
            for tup in url_list:
                if tup[2]!=0:
                    self.url.append(tup[0])
                    self.word.append(tup[1])
                    uid = tup[0].split('/')[3]
                    id = tup[0].split('/')[4].split('?')[0]
                    self.url_list.append(url_sign1.format(id, uid))
                    self.url_sign.append(url_sign2.format(id, uid) + "&max_id={}")
            self.connect.commit()  # 执行事务
            print("数据提取更新成功")
        except Exception as e:
            self.connect.rollback()
            print("数据提取失败")
            print(e)
    name = "comment"
    allowed_domains = ["weibo.com"]
    custom_settings = {
        'ITEM_PIPELINES': {
            "weibo_scrapy.pipelines.CommentScrapyPipeline": 300,
        },
        'COOKIES_ENABLED' : False
    }


    def start_requests(self):
        num =0
        for url in self.url_list:
            yield Request(url=url, callback=self.parse,meta={'num':num})
            num =num + 1

    def parse(self, response, **kwargs):
        # 请求传参
        num = response.meta['num']
        # print(response.text)
        items =CommentItem()
        json_text = json.loads(response.text)
        max_id=json_text['max_id']
        data = json_text['data']
        for i in data:
            #博主
            items['comment_writer'] = i['user']['screen_name']
            #时间
            tm = i['created_at']
            dt = datetime.datetime.strptime(tm.replace("+0800 ", ""), "%a %b %d %H:%M:%S %Y")
            # 显示秒
            tm = dt.strftime("%Y-%m-%d %H:%M:%S")
            # tm = dt.strftime("%Y-%m-%d %H:%M")
            items['comment_time'] = tm
            #评论数
            items['total_num'] = i['total_number']
            #点赞数
            items['comment_like_num'] = i['like_counts']
            #评论内容
            items['comment_content'] = i['text_raw']
            #地址
            if 'source' in i:
                items['comment_source'] = i['source'][2:]
            else:
                i['source']='无'
                items['comment_source']="无"
            # 评论文章地址
            items['comment_text_url']=self.url[num]
            #文章搜索关键词
            items['text_word'] = self.word[num]
            # print(items['text_word'])
            yield items
            # print(i['user']['screen_name'] + " " + i['text_raw'] + " " + i['created_at'] + " " + i['source'] + " " + str(i['total_number']) + " " + str(i['like_counts']))

            if i['comments'] != []:
                for j in i['comments']:
                    items['comment_writer'] = j['user']['screen_name']
                    tm = j['created_at']
                    dt = datetime.datetime.strptime(tm.replace("+0800 ",""), "%a %b %d %H:%M:%S %Y")
                    tm = dt.strftime("%Y-%m-%d %H:%M:%S")
                    # tm = dt.strftime("%Y-%m-%d %H:%M")
                    items['comment_time'] = tm
                    items['total_num'] = 0
                    items['comment_like_num'] = j['like_count']
                    items['comment_content'] = j['text_raw']
                    if 'source' in j:
                        items['comment_source'] = j['source'][2:]
                    else:
                        j['source'] = '无'
                        items['comment_source'] = "无"
                    items['comment_text_url'] = self.url[num]
                    items['text_word'] = self.word[num]
                    yield items
                    # print(j['user']['screen_name']+" "+j['text_raw']+" "+j['created_at']+" "+j['source']+" "+str(0)+" "+str(j['like_count']))
        # print(str(num+1) + " " + self.url[num])
        if max_id !=0:
            yield Request(url=self.url_sign[num].format(max_id),callback=self.parse,meta={'num':num})

