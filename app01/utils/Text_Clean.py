# -*- coding:utf-8 -*-
import jieba
import re
import csv
import emoji
import Comment_Analysis

# 创建停用词列表
def stopwordslist():
    filename = r'C:\Users\wanghuanxin\Desktop\stop_words.txt'
    stopwords = [line.strip() for line in open(filename, encoding='utf-8-sig').readlines()]
    return stopwords


def processing(text):
    text = re.sub("@.+?( |$)", "", text)
    text = re.sub("【.+?】", "", text)
    text = re.sub(".*?:", "", text)
    text = re.sub("#.*#", "", text)
    text = re.sub("\n", "", text)
    return text


# 对句子进行中文分词
def seg_depart(sentence):
    #file_path = r'C:\Users\wanghuanxin\Desktop\stop_words.txt'
    #jieba.load_userdict(file_path)
    sentence_depart = jieba.cut(sentence.strip())
    stopwords = stopwordslist()  # 创建一个停用词列表
    outstr = ''  # 输出结果为outstr
    for word in sentence_depart:  # 去停用词
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr


# 给出文档路径
filename = r"../static/form/3.csv"
output_path = r"../static/form/clean3.csv"
outputs = open(output_path, 'w', encoding='utf-8')  #输出文档路径
with open(filename, 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile,delimiter=',',quotechar='"',doublequote=False)
    for line in reader:
        line = emoji.demojize(line[0]) #将表情解码为文字，利用表情所带来的情感信息
        line_seg = seg_depart(line)
        outputs.write(line_seg + '\n')
outputs.close()
print("分词成功！！！")
