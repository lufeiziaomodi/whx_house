from django.db import models
import datetime

# Create your models here.

#
class UserInfo(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=32)

class Select(models.Model):
    num = models.IntegerField(verbose_name="选择事件序号",default=1)

class SpiderTime(models.Model):
    new = models.CharField(verbose_name="最近时间",max_length=64,default="2099-12-01")
    old = models.CharField(verbose_name="最晚时间",max_length=64,default="0000-01-01")

class HotSearch(models.Model):
    # id = models.AutoField(verbose_name="id")
    raw_hot = models.IntegerField(verbose_name="热度")
    word = models.CharField(verbose_name="标题",max_length=128,unique=True)
    category = models.CharField(verbose_name="类别",max_length=32)
    ontime = models.CharField(verbose_name="在榜时间",max_length=64)

class Comment(models.Model):
    # id = models.AutoField(verbose_name="id")
    comment_text_url = models.CharField(verbose_name="文章地址", max_length=128)
    comment_writer = models.CharField(verbose_name="博主",max_length=64)
    comment_time = models.CharField(verbose_name="发表时间",max_length=64)
    total_num = models.IntegerField(verbose_name="评论数")
    comment_like_num = models.IntegerField(verbose_name="点赞数")
    comment_content = models.TextField(verbose_name="评论内容")
    comment_source = models.CharField(verbose_name="博主位置",max_length=64)
    text_word = models.CharField(verbose_name="标题",max_length=128)
    class meta:
        unique_together =(('comment_text_url','comment_writer','comment_time'))

class Text(models.Model):
    # id = models.AutoField(verbose_name="id")
    text_writer = models.CharField(verbose_name="博主",max_length=64)
    text_word = models.CharField(verbose_name="标题", max_length=128)
    text_time = models.CharField(verbose_name="发表时间",max_length=64)
    text_forward_num = models.IntegerField(verbose_name="转发数")
    text_comment_num = models.IntegerField(verbose_name="评论数")
    text_like_num = models.IntegerField(verbose_name="点赞数")
    text_content = models.TextField(verbose_name="文章内容")
    text_url = models.CharField(verbose_name="文章地址",max_length=128,unique=True)

class Emotion(models.Model):
    e_id = models.IntegerField(verbose_name="评论数id", primary_key=True)
    sum_positive = models.IntegerField(verbose_name="积极评论数")
    sum_negtive = models.IntegerField(verbose_name="消极评论数")
    sum_positive1 = models.IntegerField(verbose_name="积极评论数")
    sum_negtive1 = models.IntegerField(verbose_name="消极评论数")
# 修改表结构
# python manage.py makemigrations
# python manage.py migrate


# 进入scrapy框架
# cd weibo_scrapy
# 运行scrapy里的weibo爬虫
# scrapy crawl weibo_search -a word="要搜索的内容"
