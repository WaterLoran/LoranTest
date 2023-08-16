import pytest
from allpairspy import AllPairs
import os
import threading

def function_to_be_tested(sex, grade, age):
    """
    作为示例,方便调试,这里至二级返回True,实际编写时候,参考下面去编写逻辑
    # if grade == "一年级" and age == "10-13岁":
    #     return False
    # return True
    :param sex:
    :param grade:
    :param age:
    :return:
    """
    return True

def is_valid_combination(row):
    """
    用于过滤正交组合对,满足则返回True,否则返回False
    :param row: 多个元素正交组合成的列表,只要按照顺序解析即可
    :return:
    """
    n = len(row)
    if n > 2:
        # 一年级 不能匹配 10-13岁
        if "一年级" == row[1] and "10-13岁" == row[2]:
            return False
    return True

class TestParameterized(object):

    parameters = [
        ["男", "女"],
        ["一年级", "二年级", "三年级", "四年级", "五年级"],
        ["8岁以下", "8-10岁", "10-13岁"]
    ]

    @pytest.mark.parametrize(["sex", "grade", "age"], [value_list for value_list in AllPairs(parameters)])
    def test_normal_scenes(self, sex, grade, age):
        print("当前进程：", os.getpid(), " 父进程：", os.getppid())
        t = threading.currentThread()
        print('Thread id : %d' % t.ident)
        assert function_to_be_tested(sex, grade, age)

    def test_print_pairs(self):
        print("当前进程：", os.getpid(), " 父进程：", os.getppid())
        print("\nPAIRWISE:")
        for i, pairs in enumerate(AllPairs(self.parameters, filter_func=is_valid_combination)):
            print("用例编号{:2d}: {}".format(i, pairs))
