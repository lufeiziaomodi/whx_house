import csv
import jieba
from app01.utils.Data_processing import Get_dict
from gensim.models import KeyedVectors
from keras.models import load_model



def tokenizer(dataset_texts):
    text = jieba.lcut(dataset_texts, cut_all=False)
    return text

def get_cba(path):
    # file_path = r'D:\python\DSU-GAN\mysite\app01\static\form\test_data.csv'
    file_path = r'C:\Users\wanghuanxin\Desktop\stop_words.txt'
    jieba.load_userdict(file_path)
    result = []
    with open(path, 'r', newline='', encoding="utf-8") as read_csvfile:
        data = csv.reader(read_csvfile, delimiter=',')
        for line in data:
            text = tokenizer(line[0])
            result.append(text)

    model = KeyedVectors.load("app01/utils/Word2vec_model.model")
    w2indx, w2vec, data = Get_dict.create_dictionaries(model, result)

    model = load_model('app01/utils/cnnbilstm.hdf5')

    y_pred = model.predict(data)

    sum_positive = 0
    sum_negtive = 0
    for i in range(len(y_pred)):
        value = y_pred[i][1]
        if (value > 0.5):
            sum_positive += 1
        else:
            sum_negtive += 1
    return sum_positive, sum_negtive
