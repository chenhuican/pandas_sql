# This started as a very thin wrapper around a file object, with intent to
# provide an object address on write() and a superblock. But as I was writing
# it, I realised that the user really wouldn't want to deal with the lengths of
# the writen chunks (and Pickle won't do it for you), so this module would have
# to abstract the file object into it's own degenerate key/value store.
# (Degenerate because you can't pick the keys, and it never releases storage,
# even when it becomes unreachable!)

import os
import struct

import portalocker

'''
physical.py ���������
1��Storage ���ṩ�־û��ļ�¼�洢��Ҳ����д��Ӳ���ϣ�
'''
class Storage(object):
    # "Q" ��ʾ�޷��ų����Σ�
    # "!" ��ʾ���������ֽ���Ҳ���Ǵ���ֽ���
    SUPERBLOCK_SIZE = 4096
    INTEGER_FORMAT = "!Q"
    INTEGER_LENGTH = 8

    def __init__(self, f):
        self._f = f
        self.locked = False
        self._ensure_superblock()

    def _ensure_superblock(self):
        #�ļ���������ֹ��������д�ļ�
        self.lock()
        # �����ļ�ĩβ
        self._seek_end()
        #�õ��ļ���ȡ��λ�ã�����ͬʱҲ���ļ���С��
        end_address = self._f.tell()
        #����ļ���СС�ڳ������С��ô����Ϊ����������㹻�Ŀռ�
        if end_address < self.SUPERBLOCK_SIZE:
            #д��һ����������
            self._f.write(b'\x00' * (self.SUPERBLOCK_SIZE - end_address))
        self.unlock()

    '''
     �����ͣ� LOCK_SH ������(Ĭ��ֵ) ���н���û��д����Ȩ�ޣ���ʹ�Ǽ�������Ҳû�С����н����ж�����Ȩ��
              LOCK_EX �������� ��������������������û�ж��Ѽ����ļ���д����Ȩ��
              LOCK_NB �������� ���ָ���˲������������ܻ���ļ������������أ����򣬺�����ȴ�����ļ�����
                      LOCK_NB����ͬLOCK_SH��LOCK_NB���а�λ��|�����������
    '''
    def lock(self):
        if not self.locked:
            portalocker.lock(self._f, portalocker.LOCK_EX)
            self.locked = True
            return True
        else:
            return False

    def unlock(self):
        if self.locked:
            self._f.flush()
            portalocker.unlock(self._f)
            self.locked = False

    def _seek_end(self):
        self._f.seek(0, os.SEEK_END)

    def _seek_superblock(self):
        self._f.seek(0)
    '''
    ��Ϊ Python ���������Ͳ��ǹ̶����ģ�����������Ҫ�õ�structģ���Ƚ� Python ��������� 8 ���ֽڣ�
    ��д�뵽�ļ���ȥ
    '''
    def _bytes_to_integer(self, integer_bytes):
        return struct.unpack(self.INTEGER_FORMAT, integer_bytes)[0]

    def _integer_to_bytes(self, integer):
        return struct.pack(self.INTEGER_FORMAT, integer)

    def _read_integer(self):
        return self._bytes_to_integer(self._f.read(self.INTEGER_LENGTH))

    def _write_integer(self, integer):
        self.lock()
        self._f.write(self._integer_to_bytes(integer))

    def write(self, data):
        self.lock()
        self._seek_end()
        object_address = self._f.tell()
        # д���ݴ�С
        self._write_integer(len(data))
        #д����
        self._f.write(data)
        # �������ݿ�ĵ�ַ
        return object_address

    def read(self, address):
        self._f.seek(address)
        length = self._read_integer() #�õ����ݴ�С
        data = self._f.read(length)
        return data

    def commit_root_address(self, root_address):
        self.lock()
        # ˢ�������������ȷ��������Ѿ�д��Ӳ��
        self._f.flush()
        # ��λ��������ĵ�ַ��Ҳ�����ļ����ڣ�
        self._seek_superblock()
        # д����ڵ�ĵ�ַ
        self._write_integer(root_address)
        self._f.flush()
        self.unlock()

    #��ȡ����¸��ڵ��ַ�뷽��
    def get_root_address(self):
        #��ȡ���ڵ��ַ
        self._seek_superblock()
        root_address = self._read_integer()
        return root_address

    def close(self):
        self.unlock()
        self._f.close()

    @property
    def closed(self):
        return self._f.closed
