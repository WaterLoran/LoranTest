import pytest
from core.logger import logger_init, logger_end
from .prepare_data import *
"""
必读:
1. sex的表示中1表示男,2表示女
"""


# @pytest.fixture(scope="module", autouse=True)
@pytest.fixture(scope="module", autouse=False)
def clean_databases_before_exec_sql():
    # 如果不存在这些表,那么久创建这些表
    delete_all_sheet()

    create_students_sheet()
    create_courses_sheet()
    create_tearchers_sheet()
    create_score_sheet()

    # 添加学生数据
    prepare_students_data()
    prepare_teachers_data()
    prepare_courses_data()
    prepare_score_data()
    print("已经清除目标的表数据,并且重新添加数据")
    pass


@pytest.fixture(scope="module", autouse=True)
def logger_mgt(request):
    logger = logger_init(request.fspath)
    logger.info("用例初始化步骤前,先根据用例的__file__来实例化一个logger")
    yield
    logger.info("用例执行结束,自动调用logger_end来解除logger的注册,避免日志打印到多个文件中")
    logger_end()
