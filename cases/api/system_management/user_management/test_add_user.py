from core.init import *
from common.ruoyi_logic import *


class TestAddUser:
    def setup(self):
        pass

    def test_add_user(self):
        reg = register({
            "user_id": None
        })
        self.reg = reg

        var_name = "hello"
        add_user(
            userName=var_name, nickName=var_name, password=var_name
        )

        lst_user(
            fetch=[reg, "user_id", f"$.rows[?(@.userName=='{var_name}')].userId"]
        )

        # 打印结果信息, 仅仅做示例
        print("\nreg.user_id\n", reg.user_id)

    def teardown(self):
        rmv_user(userId=self.reg.user_id)
        pass