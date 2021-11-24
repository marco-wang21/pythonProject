# @File  : jd_test.py
# @Author: Marco Wang
# @Date  :  2021/10/05

# -- coding: utf-8 --
import numpy as np
import pandas as pd
import requests
import time
from lxml import etree
#def get(name,x,y):
url = "https://search.jd.com/Search?keyword={}&page={}".format("维生素",1)

dic = {
    "User-Agent": ""
}
resp = requests.get(url=url,headers=dic)
resp.encoding = 'UTF-8'
resp.close()
alist=[]
blist=[]
clist=[]
#解析
html = etree.HTML(resp.text)
link =html.xpath('/html/body/div[5]/div[2]/div[2]/div[1]/div/div[2]/ul/li/div/div[1]/a/@href')
price = html.xpath('/html/body/div[5]/div[2]/div[2]/div[1]/div/div[2]/ul/li/div/div[2]/strong/i/text()')
#print(price)
a=1
for i in link:
    res= requests.get(url='https:'+str(i),headers=dic)
    res.encoding = 'UTF-8'
    res.close()
    html2=etree.HTML(res.text)
    title_ = html2.xpath('/html/body/div[6]/div/div[2]/div[1]/text()')
    title = [i.strip() for i in title_ if i.strip() != '']
    if title != []:#不为空
        alist.append(str(title[0]))
    else:
        alist.append('')
    brand = html2.xpath('/html/body/div[9]/div[2]/div[1]/div[2]/div[1]/div[1]/ul[1]/li/@title')
    if brand !=[]:
        blist.append(brand[0])
    else:
        blist.append('')
    weight = html2.xpath('/html/body/div[9]/div[2]/div[1]/div[2]/div[1]/div[1]/ul[2]/li[contains(@title,"00g")]/text()')
    #print(weight)
    if weight !=[]:
        clist.append(weight[0][5:])
    else:
        clist.append('')
    print("正在爬取第{}项".format(a))
    a+=1
    time.sleep(1)


df = pd.DataFrame({'brand': blist, 'title': alist,
                        'price': price, 'weight': clist})

time.sleep(2)

df.to_csv('test5.csv', index=False, encoding='utf_8_sig')   #导出到CSV
time.sleep(3)
df1 = pd.read_csv('./test5.csv')

df2=df1.dropna()

df2.to_csv('test6.csv', index=False, encoding='utf_8_sig')



