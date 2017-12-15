import os

from dbdb.interface import DBDB


__all__ = ['DBDB', 'connect']

'''
连接数据库函数
'''
def connect(dbname):
    try:
        f = open(dbname, 'r+b')
    except IOError:
		#os.O_RDWR 以读写的方式打开;os.O_CREAT 创建并打开一个新文件
        fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, 'r+b') #fdopen取一个现存的文件描述符
    return DBDB(f)
