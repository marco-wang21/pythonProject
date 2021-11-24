# @File  : est.py
# @Author: Marco Wang
# @Date  :  2021/10/04

# -- coding: utf-8 --
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from lxml import etree

def list(stock,x,y):
    comment_url1 = []
    comment_dict = {'view_num': [], 'comment_num': [], 'title': []}
    for i in range(x, y):
        print('爬取主页第{}页'.format(i))
        opt = Options()
        opt.add_argument("--headless")
        browser = webdriver.Chrome(options=opt)   #无头浏览器

        url = 'http://guba.eastmoney.com/list,{}_{}.html'.format(stock,i)
        browser.get(url)
        resp = browser.page_source  #拿到解析好的源代码

        html = etree.HTML(resp)

        divs = html.xpath('/html/body/div[6]/div[2]/div[4]/div')

        for div in divs[1:-2]:
            view_num = str(div.xpath('./span[1]/text()')[0])
            comment_num = str(div.xpath('./span[2]/text()')[0])
            title = str(div.xpath('./span[3]/a/text()')[0])
            comment_url ="https://guba.eastmoney.com" + str(div.xpath('./span[3]/a/@href')[0])

            comment_dict['view_num'].append(view_num)
            comment_dict['comment_num'].append(comment_num)
            comment_dict['title'].append(title)
            comment_url1.append(comment_url)  #单独把次级链接取出来

        browser.close()
    data1 = pd.DataFrame({'view_num':comment_dict['view_num'],'comment_num':comment_dict['comment_num'],
                          'titile':comment_dict['title'],'comment_url':comment_url1})
    alist = []
    for i in data1.comment_url:
        if i[-4:] != "html":
            alist.append(i)
    df2 = data1[data1['comment_url'].isin(alist)]
    df3 = data1.append(df2).drop_duplicates(keep=False)    #去除广告


    print("第一部分OK!")
    return df3


def get_comment(sub_url):
    opt = Options()
    opt.add_argument("--headless")
    browser = webdriver.Chrome(options=opt)  # 无头浏览器

    # sub_url = "https://guba.eastmoney.com/news,600221,1091060112.html"

    comment_list = []
    comment_time_list = []
    sub_comment_list = []


    browser.get(sub_url)
    resp = browser.page_source  # 拿到网页解析后的代码

    html = etree.HTML(resp)  # 解析

    post_time = str(html.xpath('/html/body/div[5]/div[3]/div[5]/div[1]/div[3]/div[2]/text()')[0])[4:-6]
    article = html.xpath('/html/body/div[5]/div[3]/div[5]/div[2]/div[2]/div/div/p/text()')
    article_ = str(','.join(article)).replace(' ', '')  # 去除空格
    divs = html.xpath('/html/body/div[5]/div[3]/div[7]/div[2]/div')
    global comment
    global sub_comment
    for div in divs:
        comment = div.xpath('./div/div/div[3]/div[2]/text()')
        sub_comment = div.xpath('./div/div/div[5]/div[2]/div[1]/div[1]/span[4]/text()')
    page_num = html.xpath('/html/body/div[5]/div[3]/div[7]/div[4]/span/span/span[1]/span/text()')

    if len(page_num) == 0:
        page_num = 1
    else:
        page_num = int(page_num[0])

    print('该标题下共{}页:'.format(page_num))
    for i in comment:
        comment_list.append(str(i))
    for j in sub_comment:
        sub_comment_list.append(str(j))
    browser.close()
    print('爬取第1页')

    if page_num > 1:
        for i in range(2, page_num + 1):
            print('爬取第{}页'.format(i))
            new_url = sub_url[:-5] + '_{}'.format(i) + sub_url[-5:]
            browser = webdriver.Chrome(options=opt)
            browser.get(new_url)
            resp = browser.page_source  # 拿到网页解析后的代码
            html = etree.HTML(resp)  # 解析
            divs = html.xpath('/html/body/div[5]/div[3]/div[7]/div[2]/div')
            for div in divs:
                comment = div.xpath('./div/div/div[3]/div[2]/text()')
                sub_comment = div.xpath('./div/div/div[5]/div[2]/div[1]/div[1]/span[4]/text()')
            for i in comment:
                comment_list.append(str(i))
            for j in sub_comment:
                sub_comment_list.append(str(j))
            browser.close()
    comment_list = ','.join(comment_list)
    sub_comment_list = ','.join(sub_comment_list)
    return article_, post_time, comment_list,  sub_comment_list

def main():
    df3  = list(600221, 1, 2)  #在此输入需要抓取的股票代码和页数
    alist=[]
    plist=[]
    clist=[]
    slist=[]
    for sub_url in df3['comment_url']:
        article_, post_time, comment_list, sub_comment_list = get_comment(sub_url)
        alist.append(article_)
        plist.append(post_time)
        clist.append(comment_list)
        slist.append(sub_comment_list)
    df4 = pd.DataFrame({'article': alist, 'post_time': plist,
                        'comment_list': clist, 'sub_comment_list': slist })

    df3.to_csv('test5.csv', index=False, encoding='utf_8_sig')
    df4.to_csv('test6.csv', index=False, encoding='utf_8_sig')   #导出到CSV


if __name__ == '__main__':
    main()

#不足：selenium速度偏慢
#或许偏慢不是坏事？

