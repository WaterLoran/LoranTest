from core.init import *
from common.ruoyi_logic import *


class TestLstSystemUser:
    def setup_class(self):
        pass

    def test_lst_system_user(self):
        reg = register({
            "rows": None
        })

        lst_system_user(
            fetch=[reg, "rows", "$.rows"]
        )

        # 打印结果信息, 仅仅做示例
        print("\nreg.rows\n", reg.rows)

    def teardown_class(self):
        pass