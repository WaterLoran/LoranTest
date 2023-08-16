from common.litemall_logic import *
from core.logger import logger_init


def test_goods_lifestyle():
    # logger = logger_init(__file__)
    # logger.info("这是TestLogger测试用例的setup部分")

    reg = register({
        my_id: None
    })

    add_goods(
        goodsSn="jincong998",
        name="jincong998_car"
    )

    lst_goods(
        name="jincong998_car",
        fetch=[[reg, "my_id", "$..data..list..id"]],
        check=["$.data.id", "eq", "888"]
    )
    # print("my_id")

    rmv_goods(
        id=reg.my_id,
    )



# 添加商品
# 查看商品
# 删除商品