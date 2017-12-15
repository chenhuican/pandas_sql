from dbdb.binary_tree import BinaryTree
from dbdb.physical import Storage

'''
	interface.py ����DBDB�࣬���Եײ�Ķ������ṹ���з�װ�����Ŵʵ�ӿ��Ѿ���ֵ����

'''
class DBDB(object):

    def __init__(self, f):
        self._storage = Storage(f)
        self._tree = BinaryTree(self._storage)

    def _assert_not_closed(self):
        if self._storage.closed:
            raise ValueError('Database closed.')

    def close(self):
        self._storage.close()

    def commit(self):
        self._assert_not_closed()
        self._tree.commit()

    def __getitem__(self, key):
		#ͨ��db[key] ��ȡ��ֵ
        self._assert_not_closed()
        return self._tree.get(key)

    def __setitem__(self, key, value):
		#ͨ��db[key] =value ���ü�ֵ
        self._assert_not_closed()
        return self._tree.set(key, value)

    def __delitem__(self, key):
		#ͨ�� del db[key] ɾ����ֵ
        self._assert_not_closed()
        return self._tree.pop(key)

    def __contains__(self, key):
		#ͨ��key in db ���жϼ��ڲ������ݿ���
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    def __len__(self):
        return len(self._tree)
