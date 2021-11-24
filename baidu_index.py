# @File  : baidu_index.py
# @Author: Marco Wang
# @Date  :  2021/10/17

# -- coding: utf-8 --

import pandas as pd
import numpy as np
from datetime import datetime

import requests
import sys
import time
from numpy import *
word_url = 'http://index.baidu.com/api/SearchApi/thumbnail?area=0&word={}'
COOKIES=''
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': COOKIES,
    'Host': 'index.baidu.com',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://index.baidu.com/v2/main/index.html',
    'User-Agent': '',
    'X-KL-Ajax-Request': 'Ajax_Request',
}




z = pd.DataFrame()

def decrypt(t, e):
    n = list(t)
    i = list(e)
    a = {}
    result = []
    ln = int(len(n) / 2)
    start = n[ln:]
    end = n[:ln]
    for j, k in zip(start, end):
        a.update({k: j})
    for j in e:
        result.append(a.get(j))
    return ''.join(result)


def get_ptbk(uniqid):
    url = 'http://index.baidu.com/Interface/ptbk?uniqid={}'
    resp = requests.get(url.format(uniqid), headers=headers)
    if resp.status_code != 200:
        print('获取uniqid失败')
        sys.exit(1)
    return resp.json().get('data')


def get_index_data(keyword,start, end,indcd):
    try:
        keyword = str(keyword).replace("'", '"')
        url = f'http://index.baidu.com/api/SearchApi/index?area=0&word={keyword}&area=0&startDate={start}&endDate={end}'

        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print('获取指数失败')
            sys.exit(1)

        content = resp.json()
        data = content.get('data')
        user_indexes = data.get('userIndexes')[0]
        uniqid = data.get('uniqid')
        ptbk = get_ptbk(uniqid)

        while ptbk is None or ptbk == '':
            ptbk = get_ptbk(uniqid)

        all_data = user_indexes.get('all').get('data')
        result = decrypt(ptbk, all_data)
        result = result.split(',')

        print(result)
        print(len(result))
        print(indcd)
       # u=len(result)

        z[indcd] = result

        # sum = 0
        # for i in result:
        #     sum = sum+float(i)
        # x= sum/u
        # print(x)
        #
        #clist.append(result)

    except:

        z[indcd] = 0
        print(indcd)








if __name__ == '__main__':
    a = pd.read_excel('./dataset7.xlsx', dtype=object)
    # a = a.drop(labels=(a.loc[a['交易年度'] < '2011'].index), axis=0)
    alist = a['indcd'].values.tolist()

    #blist = a['交易年度'].values.tolist()
    # for i in range(0, 1000):
    #     keyword = alist[i]
    #     start = blist[i] + '-01' + '-01'
    #     end = blist[i] + '-12' + '-31'
    #     #print(keyword, start, end)
    #
    #     words = [[{"name": keyword, "wordType": 1}]]
    #     start= start
    #     end= end
    #     get_index_data(words,start,end)
    #     print("第{}条完成！".format(i))
    #     time.sleep(0.5)
    for i in range(3000,len(alist)):
        keyword = alist[i]
        indcd= keyword
        words = [[{"name": keyword, "wordType": 1}]]
        start = '2011-01-01'
        end = '2020-12-31'

        get_index_data(words,start,end,indcd)
        print("第{}条完成！".format(i))
    #print(clist)
    # df = pd.DataFrame({'focus': clist})

    z.to_excel('test13.xlsx',index=False,encoding='urf8_sig')


