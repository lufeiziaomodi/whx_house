import pandas as pd
from snownlp import SnowNLP
def get_sentiment_cn(text):
    s = SnowNLP(text)
    return s.sentiments

def snownlp_anlysis(path):
    # path = r"../static/form/test_data.csv"
    df = pd.read_csv(path, names=["comments"], encoding="utf-8")
    df['sentiment'] = df.comments.apply(get_sentiment_cn)
    sum_positive = 0
    sum_negative = 0
    for i in df.sentiment:
        if i > 0.5: #积极情绪
            sum_positive += 1
        else: #消极情绪
            sum_negative += 1
    return sum_positive, sum_negative

