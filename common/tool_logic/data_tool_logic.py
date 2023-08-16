import random
from core.logic.json_data import JsonData  # 主要用于业务脚本层去获取数据回来后, 然后处理CRUD

def edit_json_data(json_data=None, **kwargs):
    JsonData().edit(json_data=json_data, **kwargs)

def generate_random_string(random_length=12):
    """
    生成一个指定长度的随机字符串
    """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(random_length):
        random_str += base_str[random.randint(0, length)]
    return random_str




