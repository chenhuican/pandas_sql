#coding:utf-8
'''
parse_station.py
获取中文站点 对应的编码 ,存为:stations.py
Usage:python parse_station.py >stations.py

'''
import re
import requests
import os
import codecs
from pprint import pprint
import sys
#reload(sys)
#sys.setdefaultencoding("utf-8")

def get_stations(url,saved_file):
	response = requests.get(url,verify=False)
	stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
	#pprint(dict(stations),indent=4)
	str_sta = 'stations='+str(dict(stations))
	paths   = os.path.abspath(__file__)
	file_paths = os.path.split(paths)[0]
	print('File: %s is saved files in path: %s'%(saved_file,file_paths))

	with codecs.open(os.path.join(file_paths,saved_file),'w',encoding='utf-8') as f:
		f.write(str_sta)

if __name__ == '__main__':
	url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.897'
	saved_file = 'stations.py'
	get_stations(url,saved_file)