from urllib.parse import quote
import json
def get_data(params):
    """
    将标准的url格式参数转换为字典
    :param params: url参数字符串
    :return: 转换后的字典
    这里可以直接字典转化为json
    """
    if params is None or params == '':
        # 如果是空或者空字符串，都返回None
        return None
    else:
        params_dict = {}
        # 分割url字符串的键值对
        list_params = params.split('&')
        # 遍历键值对
        for items in list_params:
            # 如果键值对里面有'='，那么我们就取=左边为键，=右边为值
            # 主要是支持值里面传'='
            if items.find('=') >= 0:
                params_dict[quote(items[0:items.find('=')])] = quote(items[items.find('=') + 1:])
            else:
                # 如果没有=，处理为键，值为空
                params_dict[quote(items)] = None

        print(params_dict)
        return json.dumps(params_dict)

a= get_data("username=Tester55&pwd=123456&nickname=测试账号&describe=这个账号，是一个测试注册的账号"
)
print(a)
print(type(a))