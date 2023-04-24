from scrapy.spiders import Spider
from scrapy import Request
import json
import argparse
import datetime
from urllib import parse

from weibo_scrapy.items import HotSearchItem


# # 初始化参数构造器
# parser = argparse.ArgumentParser()
# # 在参数构造器中添加两个命令行参数
# parser.add_argument('--name', type=str, default='Siri')
#
# # 获取所有的命令行参数
# args = parser.parse_args()
#
# print('Hi ' + str(args.name) )


class HotSearchSpider(Spider):
    name = "hotsearch"
    allowed_domains = ["www.weibo.com"]
    # 热搜
    custom_settings ={'ITEM_PIPELINES' : {
        "weibo_scrapy.pipelines.HotSearchScrapyPipeline": 300,
    }}
    main_urls = ["https://weibo.com/"+'ajax/side/hotSearch']

    def start_requests(self):
        yield Request(url=self.main_urls[0],callback=self.parse)
    def parse(self, response, **kwargs):
        json_text=json.loads(response.text)
        items = HotSearchItem()
        data = json_text['data']['realtime']
        # url = 'https://s.weibo.com/weibo?q={}'
        for l1 in data:
            if l1 is not None:
                if ('raw_hot' in l1):
                    items['raw_hot'] = l1['raw_hot']
                    items['word'] = l1['word']
                    items['category'] = l1['category']
                    # print(datetime.datetime.fromtimestamp(l1['onboard_time']).strftime("%Y-%m-%d %H:%M"))
                    items['ontime']=datetime.datetime.fromtimestamp(l1['onboard_time']).strftime("%Y-%m-%d %H:%M")
                    # print(str(items['raw_hot'])+" "+items['word']+" "+items['category']+" "+items['ontime'])
                    yield items
