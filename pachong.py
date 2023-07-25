import requests
from bs4 import BeautifulSoup
import time
from pyquery import PyQuery as pq
import random

import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud
import numpy as np
from collections import Counter

# 定义目前已经获取了多少篇文章
get_newcount = 0
# 获取10篇文章
new_max = 10


# 获取全部页的网址
def All_url(url):
    global get_newcount
    global new_max

    page = 1

    while page <= 3 and get_newcount < new_max:
        urls = r"https://www.chinairn.com/news/moref" + str(page) + ".html"
        print("正在爬取第%d页。" %( page ))
        print(urls)
        page = page + 1

        get_one_page(urls)


# 获取每页源代码
def get_one_page(urls):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183'}
    r = requests.get(urls, headers=headers)  # 保证不受服务器反爬虫限制
    r.encoding = r.apparent_encoding  # 保证获取源代码中的中文能正常显示
    html = r.text
    parse_one_page(html)


# 解析每页网页源代码，并获取新闻链接与新闻标题
def parse_one_page(html):
    global get_newcount
    global new_max

    count = 0

    soup = BeautifulSoup(html, 'html.parser')
    news = soup.select('.list ul li dl dt a')

    content = ""

    for new in news:
        link = new['href']  # 获取html中所需要部分的新闻链接
        news_link = 'http://news.chinairn.com/News/moref9fff' + link
        news_title = new.string  # 获取html中所需要部分的新闻名字
        print(news_link)
        print(news_title)
        count = count + 1  # 统计每页爬取的的数量
        print('正在爬取第%d篇' % (count))
        content = content + "" + parser_more_page(news_link, news_title) + "\n\n"

        get_newcount = get_newcount + 1
        print(get_newcount)

        if get_newcount > new_max:
            break

    file_path = 'news_' + str(random.randint(1000, 9999)) + '.txt'
    save_file(file_path, content)
    #
    # 对爬取的结果，进行词云分析，并得出分析结果
    showanalyse(content)

    wc = makewordcloud(content)
    showp(wc)


# 获取所有页数的新闻内容
def parser_more_page(news_link, news_title):
    res = requests.get(news_link)
    res.encoding = res.apparent_encoding
    texts = res.text
    doc = pq(texts)
    new_content = doc('.nylt .article p').text()

    return new_content


# 将读取的新闻，保存为文本文件
def save_file(file_path, content):
    file = open(file_path, "a", encoding='utf-8-sig')
    # 加上encoding参数，保证存储在txt与csv文件中中文字符不乱码
    file.write(content + '\n' + '\n')
    file.close()
    print("生成内容文件")


# 将文本进行词云次云分析，并生成结果
def makewordcloud(text):
    # 1.读入txt文本数据
    # text = open(r'test.txt', "r").read()
    # print(text)
    # 2.结巴中文分词，生成字符串，默认精确模式，如果不通过分词，无法直接生成正确的中文词云
    cut_text = jieba.cut(text)

    # print(type(cut_text))
    # 必须给个符号分隔开分词结果来形成字符串,否则不能绘制词云
    result = " ".join(cut_text)

    # print(result)

    # print(result)
    # 3.生成词云图，这里需要注意的是WordCloud默认不支持中文，所以这里需已下载好的中文字库
    # 无自定义背景图：需要指定生成词云图的像素大小，默认背景颜色为黑色,统一文字颜色：mode='RGBA'和colormap='pink'
    wcheight = 400
    wcwidth = 400
    x, y = np.ogrid[:wcwidth, :wcheight]
    mask = (x - wcwidth / 2) ** 2 + (y - wcheight / 2) ** 2 > (wcwidth / 2) ** 2
    mask = 255 * mask.astype(int)

    wc = WordCloud(
        font_path='fonts/simhei.ttf',
        # 设置字体，不指定就会出现乱码
        # 设置背景色
        background_color='white',
        # 设置背景宽
        width=wcwidth,
        # 设置背景高
        height=wcheight,
        # 最大字体
        max_font_size=50,
        # 最小字体
        min_font_size=10,
        mode='RGBA',
        # colormap='pink',
        repeat=True,
        mask=mask
    )
    # 产生词云
    wc.generate(result)
    # 保存图片
    wc.to_file(r"wordcloud.png")  # 按照设置的像素宽高度保存绘制好的词云图，比下面程序显示更清晰

    return wc


# 配置plt,否则会显示乱码
def setplt():
    plt.rcParams['font.sans-serif'] = ['SimHei']

    plt.rcParams['font.serif'] = ['SimHei']

    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题,或者转换负号为字符串


# 对分析的词云结果做词云图展示
def showp(wc):
    setplt()

    # 4.显示图片
    # 指定所绘图名称
    plt.figure("新闻词云")
    # 以图片的形式显示词云
    plt.imshow(wc)
    # 关闭图像坐标系
    plt.axis("off")
    plt.show()


# 显示词分分析结果，使用jieba模块，进行分析，得到分析结果
def showanalyse(text):
    cut_text = jieba.cut(text)

    words_result = list(cut_text)

    showresult(words_result)


# 对词云结果做条形图展示
def showresult(wc):
    setplt()

    tongji = Counter(wc).most_common(20)

    d = {key: value for (key, value) in tongji}

    rem = ['，', '、', '。', '的', '和', '\u3000', '图', '串', '“', '”', ' ', '与', '是', '端', '在', '中', '了', '\n']

    for i in list(d.keys()):
        if i in rem:
            d.pop(i)
    print(d)
    label = list(d.keys())
    y = list(d.values())
    idx = np.arange(len(y))
    plt.barh(idx, y)
    plt.yticks(idx + 0.4, label)
    plt.xlabel('出现次数', fontsize=20, labelpad=5)
    plt.ylabel('关键词', fontsize=20, labelpad=5)
    plt.title('新闻词云分析结果', fontsize=25)
    plt.savefig('输出词频图标')
    plt.show()


# 主函数
def main():
    # 爬取中研网新闻
    url = 'http://news.chinairn.com/News/moref9fff1.html'
    All_url(url)


# 主入口
if __name__ == "__main__":
    s = time.time()
    main()
    e = time.time()
    print("完成！！时间为：{}".format(e - s))
