import jieba
import pandas as pd
path = r'C:\Users\wanghuanxin\Desktop\stop_words.txt'
jieba.load_userdict(path)

def tokenizer(dataset_texts):
    text = [jieba.lcut(document.replace('\n', '')) for document in dataset_texts]
    return text
