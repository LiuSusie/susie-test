# 设置一个类，到时候实例化对象用来储存提取参数的值
class g_var(object):
    _globar_dict = {}

    # 只能改变key的值，不能改key名
    def set_dict(self, key, value):
        self._globar_dict[key] = value
        # self._globar_dict.get(key) =value，get方法不可用于修改key值，所以会报错

    def get_dict_value(self, key):
        return self._globar_dict.get(key)

    def show_dict(self):
        return self._globar_dict

