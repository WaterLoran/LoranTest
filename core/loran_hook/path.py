import os

BASE_PATH = os.getcwd()
# 这里需要适配pycharm环境下执行单个脚本的情况, 和使用run_api_case的情况
# 修改前 pycharm: BASE_PATH D:\LoranTest\cases\api\process\architecture\new
# 修改前 run_api_case: BASE_PATH D:\LoranTest
if not BASE_PATH.endswith("LoranTest"):
    while not BASE_PATH.endswith("LoranTest"):
        BASE_PATH = os.path.dirname(BASE_PATH)
CONFIG_PATH = os.path.join(BASE_PATH, 'config')
LOG_PATH = os.path.join(BASE_PATH, 'logs')

print("==================================  loran_hook中的打印")
print("BASE_PATH", BASE_PATH)
print("CONFIG_PATH", CONFIG_PATH)
print("LOG_PATH", LOG_PATH)
print("==================================  loran_hook中的打印")


