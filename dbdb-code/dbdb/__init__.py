import os

from dbdb.interface import DBDB


__all__ = ['DBDB', 'connect']

'''
�������ݿ⺯��
'''
def connect(dbname):
    try:
        f = open(dbname, 'r+b')
    except IOError:
		#os.O_RDWR �Զ�д�ķ�ʽ��;os.O_CREAT ��������һ�����ļ�
        fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, 'r+b') #fdopenȡһ���ִ���ļ�������
    return DBDB(f)
