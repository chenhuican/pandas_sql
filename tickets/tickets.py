#!/usr/bin/env python
#coding:utf-8
''' 命令行火车票查看器
Usage:
	tickets [-gdtkz] <from> <to> <date>

Options:
	-h,--help   显示帮助菜单
	-g          高铁
	-d          动车
	-t          特快
	-k          快速
	-z          直达
Example:
	tickets  北京  上海 2017-12-01
	tickets  -dg   成都 南京 2017-12-01
'''
from docopt import docopt
from stations import stations
import requests
from pprint import pprint
import json
from trains_collection import TrainsCollection

def get_ticketsinfo():
	arguments = docopt(__doc__)
	#print(arguments)
	from_station = stations.get(arguments['<from>'])
	to_station   = stations.get(arguments['<to>'])
	date = arguments['<date>']
	url = ('https://kyfw.12306.cn/otn/leftTicket/query?'
			'leftTicketDTO.train_date={}&leftTicketDTO.from_station={}'
			'&leftTicketDTO.to_station={}&purpose_codes=ADULT'
		   ).format(date,from_station,to_station)
	print('Params is:',from_station,to_station,date)
	res = requests.get(url,verify=False)
	#pprint(res.json(),indent=4)
	#jsons = json.loads(res.text)
	#print(jsons)
	#json 返回json方法，json()返回json数据
	trains_json = res.json()
	print(trains_json['data'])
	options = ''.join([
		key for key,value in arguments.items() if value if True
		])
	TrainsCollection(available_trains,options).pretty_print()

def get_header():
	return 	{
		'Host':'kyfw.12306.cn',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; W…) Gecko/20100101 Firefox/55.0',
		'Accept':'*/*',
		'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
		'Accept-Encoding':'gzip, deflate, br',
		'Referer':'https://kyfw.12306.cn/otn/leftTicket/init',
		'If-Modified-Since':'0',
		'Cache-Control':'no-cache',
		'X-Requested-With':'XMLHttpRequest',
		'Connection':'keep-alive',
	}

if __name__ == '__main__':
	#url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(date,from_station,to_station)
	get_ticketsinfo()