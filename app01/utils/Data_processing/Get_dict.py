from keras.utils import pad_sequences
from gensim.corpora.dictionary import Dictionary

def create_dictionaries(model=None, data=None):
    if (data is not None) and (model is not None):
        gensim_dict = Dictionary()
        gensim_dict.doc2bow(model.wv.index_to_key,
                            allow_update=True)
        #  freqxiao10->0 所以k+1
        w2indx = {v: k + 1 for k, v in gensim_dict.items()}  # 频数超过10的词语的索引
        f = open("word2index.txt", 'w', encoding='utf-8-sig')
        for key in w2indx:
            f.write(str(key))
            f.write(' ')
            f.write(str(w2indx[key]))
            f.write('\n')
        f.close()
        w2vec = {word: model.wv[word] for word in w2indx.keys()}  # 频数超过10的词语的词向量

        def parse_dataset(combined):
            data = []
            for sentence in combined:
                new_txt = []
                for word in sentence:
                    try:
                        new_txt.append(w2indx[word])
                    except:
                        new_txt.append(0)
                data.append(new_txt)
            return data  # word=>index

        data = parse_dataset(data)
        data = pad_sequences(data, maxlen=100)
        return w2indx, w2vec, data
    else:
        print('文本为空！')
