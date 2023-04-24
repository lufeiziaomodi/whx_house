from scrapy.spiders import Spider
from scrapy import Request,Selector
import json
import argparse
import datetime
from urllib import parse
import urllib.request
import time
import re

from weibo_scrapy.items import TextItem


# 匹配#搜索内容#形式

class HotsearchtextSpider(Spider):
    name = "hotsearch_text"
    allowed_domains = ["s.weibo.com"]

    # 搜索
    def __init__(self, word='', page='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        if word == '':
            word = input('请输入要搜索的内容:')
        self.word = word
        if page == '':
            page = '1'
        self.page = int(page)
        # 综合排
        url = 'https://s.weibo.com/weibo?q={}'
        # 实时
        # url = 'https://s.weibo.com/weibo?q={}&rd=realtime&tw=realtime&Refer=weibo_realtime'
        # 格式化字符串
        query_string = parse.quote(word)
        url = url.format(query_string) + "&page={}"
        self.main_urls = []
        for i in range(self.page):
            self.main_urls.append(url.format(str(i + 1)))

    custom_settings = {
        'ITEM_PIPELINES': {
            "weibo_scrapy.pipelines.TextScrapyPipeline": 300,
        },
        "DOWNLOADER_MIDDLEWARES": {
            "weibo_scrapy.middlewares.WeiboScrapyDownloaderMiddleware": 543,
        }
    }

    def start_requests(self):
        for page_url in self.main_urls:
            # print(page_url)
            yield Request(url=page_url, callback=self.parse)

    def parse(self, response):
        # print("正在解析")
        sel = Selector(response)
        page = sel.xpath('/html/body/div[1]/div[3]/div[2]/div[1]/div[1]')
        page = page.css("div.card-wrap")
        # print(page)
        item = TextItem()
        for pos in page:
            # 博主
            text_writer_css = pos.css('div.info a.name::text').extract_first()
            if text_writer_css is None:
                continue
            text_writer = str(text_writer_css).replace('\n', '').strip()
            # print(text_writer)
            # 时间
            text_time_css = pos.css('div.content p.from a:nth-child(1)::text').extract_first()
            if text_time_css is None:
                continue
            text_time = str(text_time_css).replace('\n', '').strip()
            tm = text_time
            tm = tm.replace('\n', '').strip()
            if '人数' in tm:
                tm = tm.replace(tm.split()[-1], '').strip()
            if tm[2] == '月':
                date = datetime.date.today().strftime("%Y年")
                tm = date + tm
            if '今天' in tm:
                date = datetime.date.today().strftime("%Y年%m月%d日") + " "
                tm = tm.replace('今天', date)
            if '分钟' in tm:
                mt = tm.split("分钟前")[0]
                minute = datetime.timedelta(minutes=int(mt))
                tm = (datetime.datetime.now() - minute).strftime("%Y年%m月%d日 %H:%M")
            if '秒' in tm:
                mt = tm.split("秒前")[0]
                sencond = datetime.timedelta(seconds=int(mt))
                tm = (datetime.datetime.now() - sencond).strftime("%Y年%m月%d日 %H:%M")
            if '-' in tm:
                tm = datetime.datetime.strptime(tm, "%Y-%m-%d %H:%M").strftime("%Y年%m月%d日 %H:%M")
            text_time = datetime.datetime.strptime(tm, "%Y年%m月%d日 %H:%M").strftime("%Y-%m-%d %H:%M")
            # print(text_time)
            # 转发数
            text_forward_num = str(pos.css('div.card-act ul li:nth-child(2) a::text ').extract_first()).replace('\n',
                                                                                                                '').replace(
                '转发', '').strip()
            if text_forward_num == '':
                text_forward_num = '0'
            # 评论数
            text_comment_num = str(pos.css('div.card-act ul li:nth-child(3) a::text ').extract_first()).replace('\n',
                                                                                                                '').replace(
                '评论', '').strip()
            if text_comment_num == '':
                text_comment_num = '0'
            # 点赞数
            text_like_num = str(pos.css('div.card-act ul li span.woo-like-count::text ').extract_first()).replace('\n',
                                                                                                                  '')
            text_like_num = re.findall(r"\d+", text_like_num)
            if text_like_num == []:
                text_like_num = 0
            else:
                text_like_num = text_like_num[0]
            # 文章地址
            text_url = str(pos.css('div.content p.from a:nth-child(1)::attr(href)').extract_first()).replace('\n',
                                                                                                             '').strip()
            # 文章内容
            text_content_css = pos.css('div.card')
            text_content = ''
            for i in text_content_css:
                i = i.css('p[node-type="feed_list_content"]::text').extract()
                for j in i:
                    j = j.strip().replace('\n', '').replace('\r', '')
                    text_content = text_content + j
                text_content.strip().replace('\n', '')
            # print(text_time)
            # print(text_writer+" "+text_time+" "+text_url+" "+text_content+" "+text_forward_num+" "+text_comment_num+" "+text_like_num)
            item["text_word"] = self.word
            item["text_writer"] = text_writer
            item["text_time"] = text_time
            item["text_url"] = text_url
            item["text_content"] = text_content
            item["text_forward_num"] = text_forward_num
            item["text_comment_num"] = text_comment_num
            item["text_like_num"] = text_like_num
            # print(item)
            yield item