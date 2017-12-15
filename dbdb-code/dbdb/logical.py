'''
	���ļ��������߼��㣬���Ǽ�ֵ�����ĳ���ӿ�
	ValueRef ��ָ�����ݿ��ж��������ݶ����python����
	�Ƕ����ݿ������ݵ�����
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
        #_addressΪ0���ֱ�ӷ���_referent����_referentΪNone
        if self._referent is None and self._address:
            #�����ļ��ж�ȡ���ֽڴ�ת��Ϊpython�����õĶ���
            self._referent = self.string_to_referent(storage.read(self._address))
        return self._referent

    def store(self, storage):
        # ���ö���Ϊ�ն���ַΪ��˵�������ö���δ���洢��
        if self._referent is not None and not self._address:
            #�洢���ö���ǰ�������������Զ���
            self.prepare_to_store(storage)
            # �õ����ö������ļ��еĵ�ַ
            self._address = storage.write(self.referent_to_string(self._referent))

'''
	LogicalBase ��
    �ṩ���߼����£����� get��set �Լ� commit���ĳ���ӿڣ�
    ��ͬʱ�������洢��������Լ����ڲ��ڵ�Ľ�����
'''
class LogicalBase(object):
    # �����ݽṹ�ڵ�����ã����������и�ֵ BinaryNodeRef
    node_ref_class = None
    #��ֵ������
    value_ref_class = ValueRef

    def __init__(self, storage):
        self._storage = storage
        self._refresh_tree_ref()

    #�ύ����
    def commit(self):
        #�洢���õ���
        self._tree_ref.store(self._storage)
        #���������ڵ�ĵ�ַ
        self._storage.commit_root_address(self._tree_ref.address)

    '''
    _refresh_tree_ref��ͨ����ȡ�ļ��еĸ��ڵ��ַ��ˢ�����ĸ��ڵ㡣
    �´������ļ���һ���������㣬��ô����õ��ĸ���ַҲ����0�ˣ�
    C������ȫΪ���ָ����ǿ�ָ�룬����������Ҳ�������ɵ�ַΪ0�������Ǹ�������
    '''
    def _refresh_tree_ref(self):
        self._tree_ref = self.node_ref_class(
            address=self._storage.get_root_address())

    def get(self, key):
        # ������ݿ��ļ�û������������¶���������
        if not self._storage.locked:
            self._refresh_tree_ref()
            # _get ��������������ʵ��
        return self._get(self._follow(self._tree_ref), key)

    def set(self, key, value):
        if self._storage.lock():
            self._refresh_tree_ref()
            #_insert ��������������ʵ��
        self._tree_ref = self._insert(
            self._follow(self._tree_ref), key, self.value_ref_class(value))
    #ɾ����ֵ
    def pop(self, key):
        if self._storage.lock():
            self._refresh_tree_ref()
        #_delete ��������������ʵ��
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
