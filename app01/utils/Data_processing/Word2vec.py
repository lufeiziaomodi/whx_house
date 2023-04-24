from gensim.models.word2vec import Word2Vec
import multiprocessing


cpu_count = multiprocessing.cpu_count()
vocab_dim = 100 #特征维度
n_exposures = 10  # 所有频数超过10的词语
window_size = 7   #上下文最大距离

def word2vec_train(data):
    model = Word2Vec(vector_size=vocab_dim,
                     min_count=n_exposures,
                     window=window_size,
                     workers=cpu_count,)
    model.build_vocab(data)  # input: list
    model.train(data, total_examples=model.corpus_count, epochs=1)
    #model.save('Word2vec_model.model')
