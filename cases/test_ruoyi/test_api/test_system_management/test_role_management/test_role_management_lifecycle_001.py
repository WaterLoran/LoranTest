# coding=utf8
import time
import random
from common.ruoyi_logic import *


CASE_ID = "test_role_management_lifecycle_001"


def _uid(case_id):
    ts = int(time.time())
    rnd = random.randint(100, 999)
    return f"{case_id}_{ts}_{rnd}"


class TestRoleManagementLifecycle001:
    def setup_method(self):
        self.reg = register({"role_id": None})

    def test_role_management_lifecycle_001(self):
        reg = self.reg
        rname = _uid("lifecycle_001")
        add_role(
            roleName=rname,
            roleKey=rname,
            roleSort=6,
            menuIds=[1, 100, 1000],
            remark="备注内容",
            check=[["$.code", "eq", 200]],
        )
        lst_role(
            roleName=rname,
            pageSize=100,
            fetch=[reg, "role_id", f"$.rows[?(@.roleName=='{rname}')].roleId"],
            check=[
                ["$.code", "eq", 200],
                [f"$.rows[?(@.roleName=='{rname}')]", "exist", True],
            ],
        )
        assert reg.role_id is not None, "应能查到刚创建的角色"

    def teardown_method(self):
        reg = self.reg
        if getattr(reg, "role_id", None):
            try:
                rmv_role(role_id=reg.role_id)
            except Exception as e:
                print(f"清理角色失败: {e}")
