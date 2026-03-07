# coding=utf8
from common.ruoyi_logic import *
import time
import random


class TestAddUser998:
    def setup_method(self):
        pass

    def test_add_user_998(self):
        # 生成唯一用户名，避免重复
        timestamp = int(time.time())
        random_suffix = random.randint(1000, 9999)
        var_name = f"testuser_{timestamp}_{random_suffix}"
        
        reg = register({
            "user_id": None,
            "user_id2": None,
        })
        self.reg = reg

        # 添加用户
        add_user(
            userName=var_name, 
            nickName=var_name, 
            password=var_name,
            check=[
                ["$.msg", "eq", "操作成功"],
                ["$.code", "==", 200],
                ["msg", "eq", "操作成功"]
            ],
        )

        # 查看用户
        lst_user(
            fetch=[
                [reg, "user_id", f"$.rows[?(@.userName=='{var_name}')].userId"],
                [reg, "user_id2", f"$.rows[?(@.userName=='{var_name}')].userId"],
            ],
            check=[f"$.rows[?(@.userName=='{var_name}')].nickName", "eq", var_name]
        )

        print("reg.user_id", reg.user_id)

    def teardown_method(self):
        # 删除用户 - 只有在成功获取到用户ID时才执行
        if self.reg.user_id:
            rmv_user(
                userId=self.reg.user_id,
                check=[
                    ["$.msg", "eq", "操作成功"],
                    ["$.code", "==", 200],
                ],
            )
        else:
            print("teardown: 未获取到用户ID，跳过删除")
