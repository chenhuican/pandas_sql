#-*- coding:utf-8 -*-
#读取山东FDA的药品GSP认证经营企业数据
# 20161128 zhangshaohua
import re
import requests
import json
from pprint import pprint
 
 
#读取首页
url = 'http://124.128.39.251:9080/sdfdaout/jsp/datasearch/searchinfolist.jsp?pageSize=10&entType=drugGSP&thisPage=1'
url = 'http://124.128.39.251:9080/sdfdaout/jsp/datasearch/searchinfolist.jsp?pageSize=10&thisPage=2&entType=drugGSP'
#url = 'http://124.128.39.251:9080/sdfdaout/jsp/datasearch/searchinfolist.jsp?pageSize=10&thisPage=12&entType=drugGSP'
#取总记录数,每页20条#zjls = getContent(url,'共(\d{1,5})页','UTF-8')
headers = {
'Host': '124.128.39.251:9080',
'Proxy-Connection': 'keep-alive',
'Content-Length': '256',
'Origin': 'http://124.128.39.251:9080',
'X-Requested-With': 'XMLHttpRequest',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
'Content-Type': 'application/json',
'Accept': '*/*',
'Referer': 'http://124.128.39.251:9080/sdfdaout/jsp/datasearch/searchinfolist.jsp',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.8',
 
}
 
url = 'http://124.128.39.251:9080/sdfdaout/command/ajax/com.lc.datasearch.cmd.SearchInfoQueryCmd'
parms = {"params":{"javaClass":"org.loushang.next.data.ParameterSet","map":{"limit":10,"start":10,"entType":"drugGSP","defaultSort":{"javaClass":"ArrayList","list":[]},"dir":"ASC","needTotal":True},"length":7},"context":{"javaClass":"HashMap","map":{},"length":0}}
values = json.dumps(parms)
req = requests.post(url,data=values,headers=headers)
content = req.json()
pprint(content,indent=4)
 
#print(type(content))
print('药品零售企业读取完成！')