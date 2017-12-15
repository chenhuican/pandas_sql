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
physical.py 定义物理层
1，Storage 类提供持久化的记录存储（也就是写到硬盘上）
'''
class Storage(object):
    # "Q" 表示无符号长整形，
    # "!" 表示网络流的字节序，也就是大端字节序
    SUPERBLOCK_SIZE = 4096
    INTEGER_FORMAT = "!Q"
    INTEGER_LENGTH = 8

    def __init__(self, f):
        self._f = f
        self.locked = False
        self._ensure_superblock()

    def _ensure_superblock(self):
        #文件上锁，防止其它进程写文件
        self.lock()
        # 到达文件末尾
        self._seek_end()
        #得到文件读取的位置（这里同时也是文件大小）
        end_address = self._f.tell()
        #如果文件大小小于超级块大小那么必须为超级块分配足够的空间
        if end_address < self.SUPERBLOCK_SIZE:
            #写入一串二进制零
            self._f.write(b'\x00' * (self.SUPERBLOCK_SIZE - end_address))
        self.unlock()

    '''
     锁类型： LOCK_SH 共享锁(默认值) 所有进程没有写访问权限，即使是加锁进程也没有。所有进程有读访问权限
              LOCK_EX 排他锁。 除加锁进程外其他进程没有对已加锁文件读写访问权限
              LOCK_NB 非阻塞锁 如果指定此参数，函数不能获得文件锁就立即返回，否则，函数会等待获得文件锁。
                      LOCK_NB可以同LOCK_SH或LOCK_NB进行按位或（|）运算操作。
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
    因为 Python 的整数类型不是固定长的，所以我们需要用到struct模块先将 Python 整数打包成 8 个字节，
    再写入到文件中去
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
        # 写数据大小
        self._write_integer(len(data))
        #写数据
        self._f.write(data)
        # 返回数据块的地址
        return object_address

    def read(self, address):
        self._f.seek(address)
        length = self._read_integer() #得到数据大小
        data = self._f.read(length)
        return data

    def commit_root_address(self, root_address):
        self.lock()
        # 刷新输出缓冲区，确认输出都已经写到硬盘
        self._f.flush()
        # 定位到超级块的地址（也就是文件开口）
        self._seek_superblock()
        # 写入根节点的地址
        self._write_integer(root_address)
        self._f.flush()
        self.unlock()

    #获取与更新根节点地址与方法
    def get_root_address(self):
        #获取根节点地址
        self._seek_superblock()
        root_address = self._read_integer()
        return root_address

    def close(self):
        self.unlock()
        self._f.close()

    @property
    def closed(self):
        return self._f.closed
