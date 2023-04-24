from scrapy import cmdline
#在我们scrapy项目里面，为了方便运行scrapy的项目的时候创建的文件
#使用cmdlie.execute()方法执行爬虫启动命令：scrapy crawl 爬虫名

#execute方法需要运行的每一个命令为单独的一个字符串，如：cmdline.execute(['scrapy', 'crawl', 'tubatu'])，所以如果命令为一整个字符串时，需要split( )进行分割；#**
# cmdline.execute("scrapy crawl comment".split())
# cmdline.execute("scrapy crawl hotsearch_text -a word=#四级# -a page=5".split())
# cmdline.execute("scrapy crawl search -a word=四级 -a page=5".split())
cmdline.execute("scrapy crawl hotsearch_text -a word=#蓝桥杯# -a page=4".split())
# cmdline.execute("scrapy crawl hotsearch".split())