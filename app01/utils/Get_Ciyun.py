import matplotlib.pyplot as plt
from wordcloud import WordCloud
path = r'../static/form/clean5.csv'
text = open(path, encoding="utf-8").read()  # 标明文本路径，打开

# 生成对象
wc = WordCloud(font_path="C:\Windows\Fonts\Microsoft YaHei UI\msyh.ttc", width=500, height=400,
               colormap='cool', mode="RGBA", background_color=(0,0,0,0), collocations=False).generate(text)
# 显示词云图
plt.imshow(wc)
plt.axis("off")
plt.savefig("../static/img/ciyun5")
plt.show()
