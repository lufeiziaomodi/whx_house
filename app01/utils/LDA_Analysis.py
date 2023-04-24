from gensim.models import LdaModel
from gensim import corpora, models
import pyLDAvis.gensim_models as gensims
import pyLDAvis
# 准备数据
PATH = "../static/form/clean5.csv"

file_object2 = open(PATH, encoding='utf-8', errors='ignore').read().split('\n')  # 一行行的读取内容
data_set = []  # 建立存储分词的列表
for i in range(len(file_object2)):
    result = []
    seg_list = file_object2[i].split()
    for w in seg_list:  # 读取每一行分词
        result.append(w)
    data_set.append(result)

dictionary = corpora.Dictionary(data_set)  # 构建 document-term matrix
corpus = [dictionary.doc2bow(text) for text in data_set]

lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=4, passes=30, random_state=1)
topic_list = lda.print_topics()
# print(topic_list)

result_list = []
for i in lda.get_document_topics(corpus)[:]:
    listj = []
    for j in i:
        listj.append(j[1])
    bz = listj.index(max(listj))
    result_list.append(i[bz][0])
#print(result_list)
data = gensims.prepare(lda, corpus, dictionary)
#pyLDAvis.show(data)
pyLDAvis.save_html(data, "../templates/event5.html")