import numpy as np
import keras
from sklearn.model_selection import train_test_split

def get_data(w2indx, w2vec, data, y):
    n_symbols = len(w2indx) + 1  # 补上索引为0（频数小于10）的词
    embedding_weights = np.zeros((n_symbols, 100))
    for word, index in w2indx.items():
        embedding_weights[index, :] = w2vec[word]
    x_train, x_test, y_train, y_test = train_test_split(data, y, test_size = 0.99) #test_size模型训练为0.2
    y_train = keras.utils.to_categorical(y_train, num_classes=2)  # 转换为one-hot特征
    y_test = keras.utils.to_categorical(y_test, num_classes=2)
    return n_symbols, embedding_weights, x_train, y_train, x_test, y_test
