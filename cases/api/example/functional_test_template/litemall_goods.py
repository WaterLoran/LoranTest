from common.litemall_logic import *
from core.logger import logger_init


def test_goods_lifestyle():
    logger = logger_init(__file__)
    logger.info("这是TestLogger测试用例的setup部分")

    add_goods(
        goodsSn="jincong998",
        name="jincong998_car"
    )
    my_id = lst_goods(
        name="jincong998_car",
        fetch=[["my_id", "$..data..list..id"]]
    )
    print("my_id", my_id)
    rmv_goods(
        id=my_id,
    )

    print("my_id", my_id)
