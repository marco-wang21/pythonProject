# @File  : bs_test.py
# @Author: Marco Wang
# @Date  :  2021/11/15

# -- coding: utf-8 --
import pandas as pd
import numpy as np
from scipy.stats import norm
def vanilla_option(S, K, T, r, sigma, option='call'):   #bs公式
    # S: 现价
    # K: 行权价
    # T: 距离到期时间
    # r: 无风险利率
    # sigma: 波动率
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2 = (np.log(S/K) + (r - 0.5*sigma**2)*T)/(sigma * np.sqrt(T))

    if option == 'call': #看涨
        p = (S*norm.cdf(d1, 0.0, 1.0) - K*np.exp(-r*T)*norm.cdf(d2, 0.0, 1.0))

    elif option == 'put': #看跌
        p = (K*np.exp(-r*T)*norm.cdf(-d2, 0.0, 1.0) - S*norm.cdf(-d1, 0.0, 1.0))
    else:
        return None
    return p

b = pd.read_excel('./Temp.xlsx')
a = pd.read_excel('./Temp2.xlsx')
a = a.rename(columns={'收盘价(元)':'end_price'})
a['log_ret'] = np.log(a['end_price']/ a['end_price'].shift(1))   #对数收益率
a['volatility']  =a['log_ret'].rolling(window=242,center=False).std()   #波动率
a['volatility_year']  =a['volatility'] * np.sqrt(242)   #年化波动率  假定一年交易日242天
a = a.rename(columns={'日期':'date'})
a = a.rename(columns={'代码':'code'})
a = a.rename(columns={'名称':'stock_name'})
d=pd.DataFrame(a, columns=['code','stock_name','date','end_price','log_ret','volatility','volatility_year'])

b = b.rename(columns={'日期':'date'})
b = b.rename(columns={'收盘价(元)':'warrant_price'})
b = b.rename(columns={'名称':'warrant_name'})
b = b.rename(columns={'代码':'warrant_index'})
e=pd.DataFrame(b, columns=['warrant_index','warrant_name','date','warrant_price'])


c=pd.merge(d,e,how='left')
c=c.dropna(axis=0)
c['date1'] = pd.to_datetime(c['date'])
t1 = pd.to_datetime('2021-11-19')
c['date2'] = (t1 - c['date1']).apply(lambda x: x.days)   #计算到期时间
c['date3'] = c['date2'] / 365   #将天转换为年
c['strike_price'] = 22    #已知行权价22元

g = pd.read_excel('./香港同业拆借利率(HIBOR)(日).xlsx')
g= g.dropna(axis=0)
g = g.drop(0)
g['date'] = pd.to_datetime(g['指标名称'])

h  = pd.merge(c,g,how='left')

h['interest'] = (h['HIBOR:12个月']) / 100
h['interest'] = h['interest'].apply(lambda x: float(x))
h['theory'] = vanilla_option(h['end_price'],h['strike_price'] , h['date3'], h['interest'], h['volatility_year'], option='call') #调用bs公式模块
h.to_excel('dataset1.xlsx',index=False,encoding='urf8_sig')
