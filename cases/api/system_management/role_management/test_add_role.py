from core.init import *
from common.ruoyi_logic import *


class TestAddRole:
    def setup(self):
        pass

    def test_add_role(self):
        reg = register({
            "role_id": None
        })
        self.reg = reg

        var_name = "new_role"
        add_role(
            roleName=var_name, roleKey=var_name, remark=var_name,
        )

        lst_role(
            fetch=[reg, "role_id", f"$.rows[?(@.roleName=='{var_name}')].roleId"]
        )

        # 打印结果信息, 仅仅做示例
        print("\nreg.role_id\n", reg.role_id)

    def teardown(self):
        rmv_role(roleId=self.reg.role_id)
        pass