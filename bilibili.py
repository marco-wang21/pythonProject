# @File  : bilibili.py
# @Author: Marco Wang
# @Date  :  2022/02/03

# -- coding: utf-8 --

import requests
import  jieba
import  imageio
import wordcloud
import re
import jieba


url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=499893135'    #弹幕api,通过直接在视频链接"bilibili"前加入“i”获取
dic = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
}

resp = requests.get(url=url, headers = dic)
resp.encoding = 'UTF-8'
resp.close()

data_list = re.findall('<d p=".*?">(.*?)</d>',resp.text)

for index in data_list:
    with open('何同学.txt',mode='a',encoding='utf-8') as f:
        f.write(index)
        f.write('\n')

f = open('何同学.txt',encoding='utf-8')
text = f.read()

text_list = jieba.lcut(text) #分词
text_str = ' '.join(text_list)

stoplist = [i.strip() for i in open('stoplist.txt', encoding = 'utf-8').readlines()]   #stoplist
def m_cut(intxt):  #segmentation
    word = [w for w in jieba.cut(intxt) if w not in stoplist and len(w) > 1 and not re.match('^[a-z|A-Z|0-9|哈|.]*$',w)]
    strword = " ".join(word)
    return strword
cuttext = m_cut(text)


import wordcloud
import imageio  #根据本地图片修改词云图形
img2 = imageio.imread('tree.png')
wc = wordcloud.WordCloud(
    width=500,
    height=500,
    background_color = 'white',
    mask=img2 ,
    stopwords={'开始','的','地方','了','你','我','啊'},
    font_path = 'msyh.ttc',
)
wc.generate(cuttext)
wc.to_file('词云.png')

