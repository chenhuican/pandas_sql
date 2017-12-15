'''
	该文件定义了逻辑层，它是键值操作的抽象接口
	ValueRef 是指向数据库中二进制数据对象的python对象，
	是对数据库中数据的引用
'''
class ValueRef(object):
    def prepare_to_store(self, storage):
        pass

    @staticmethod
    def referent_to_string(referent):
        return referent.encode('utf-8')

    @staticmethod
    def string_to_referent(string):
        return string.decode('utf-8')

    def __init__(self, referent=None, address=0):
        self._referent = referent
        self._address = address

    @property
    def address(self):
        return self._address

    def get(self, storage):
        #_address为0则会直接返回_referent，而_referent为None
        if self._referent is None and self._address:
            #将从文件中读取的字节串转换为python中引用的对象
            self._referent = self.string_to_referent(storage.read(self._address))
        return self._referent

    def store(self, storage):
        # 引用对象不为空而地址为空说明该引用对象还未被存储过
        if self._referent is not None and not self._address:
            #存储引用对象前的其他操作，自定义
            self.prepare_to_store(storage)
            # 得到引用对象在文件中的地址
            self._address = storage.write(self.referent_to_string(self._referent))

'''
	LogicalBase 类
    提供了逻辑更新（比如 get，set 以及 commit）的抽象接口，
    它同时负责管理存储对象的锁以及对内部节点的解引用
'''
class LogicalBase(object):
    # 对数据结构节点的引用，会在子类中赋值 BinaryNodeRef
    node_ref_class = None
    #对值的引用
    value_ref_class = ValueRef

    def __init__(self, storage):
        self._storage = storage
        self._refresh_tree_ref()

    #提交数据
    def commit(self):
        #存储引用的树
        self._tree_ref.store(self._storage)
        #更新树根节点的地址
        self._storage.commit_root_address(self._tree_ref.address)

    '''
    _refresh_tree_ref会通过读取文件中的根节点地址来刷新树的根节点。
    新创建的文件是一串二进制零，那么最初得到的根地址也就是0了，
    C语言中全为零的指针就是空指针，在这里我们也可以理解成地址为0的引用是个空引用
    '''
    def _refresh_tree_ref(self):
        self._tree_ref = self.node_ref_class(
            address=self._storage.get_root_address())

    def get(self, key):
        # 如果数据库文件没有上锁，则更新对树的引用
        if not self._storage.locked:
            self._refresh_tree_ref()
            # _get 方法将在子类中实现
        return self._get(self._follow(self._tree_ref), key)

    def set(self, key, value):
        if self._storage.lock():
            self._refresh_tree_ref()
            #_insert 方法将在子类中实现
        self._tree_ref = self._insert(
            self._follow(self._tree_ref), key, self.value_ref_class(value))
    #删除键值
    def pop(self, key):
        if self._storage.lock():
            self._refresh_tree_ref()
        #_delete 方法将在子类中实现
        self._tree_ref = self._delete(
            self._follow(self._tree_ref), key)

    def _follow(self, ref):
        return ref.get(self._storage)

    def __len__(self):
        if not self._storage.locked:
            self._refresh_tree_ref()
        root = self._follow(self._tree_ref)
        if root:
            return root.length
        else:
            return 0
