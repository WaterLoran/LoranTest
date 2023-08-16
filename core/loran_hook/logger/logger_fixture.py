import pytest
from core.loran_hook.logger import logger_init, logger_end

@pytest.fixture(scope="class", autouse=True)
def logger_fixture(request):

    print("\n=======================request start=================================")
    # print('测试方法的参数化数据：{}'.format(request.param))  # 此处需要结合@pytest.mark.parameter(indirect=Ture)来使用
    print('测试方法所处模块的信息：{}'.format(request.module))
    # print('测试方法信息：{}'.format(request.function))  # 此处有可能是因为装饰的是一个类,所以这里如函数的相关信息
    print('测试方法所在的类的信息：{}'.format(request.cls))
    print('测试方法所在路径信息：{}'.format(request.fspath))
    print('测试方法调用的多个fixture函数（比如fixture函数之间的嵌套调用（包括pytest内嵌的fixture函数））信息：{}'.format(request.fixturenames))
    print('测试方法调用的单个fixture函数（自己在程序中定义在测试方法中调用的fixture函数）信息：{}'.format(request.fixturename))
    print('测试方法级别信息：{}'.format(request.scope))
    print("\n=======================request end=================================")

    logger = logger_init(request.fspath)
    logger.info("用例初始化步骤前,先根据用例的__file__来实例化一个logger")
    yield
    logger.info("用例执行结束,自动调用logger_end来解除logger的注册,避免日志打印到多个文件中")
    logger_end()

    