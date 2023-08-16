# -*- coding:utf8 -*-
import os
import argparse
import logging
from common.tool_logic.time_tool import DateTimeTool
import platform
from plugin.allure.allure_report_data import AllureFileClean
from plugin.models import NotificationType
from plugin.notify.lark import FeiShuTalkChatBot
from config import notify as notify_config
import pytest
frame_logger = logging.getLogger(__name__)

"""
提供的功能
1. 可选根据关键字去增量选择待执行脚本
2. 可选根据关键字去增量选择待执行脚本
"""

if __name__ == '__main__':

    base_path = os.getcwd()

    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--keyword', help='只执行匹配关键字的用例，会匹配文件名、类名、方法名', type=str)
    parser.add_argument('-d', '--dir', help='指定要测试的目录', type=str)
    parser.add_argument('-m', '--markexpr', help='只运行符合给定的mark表达式的测试', type=str)
    parser.add_argument('-s', '--capture', help='是否在标准输出流中输出日志,1:是、0:否,默认为0', type=str)
    parser.add_argument('-r', '--reruns', help='失败重跑次数,默认为0', type=str)
    parser.add_argument('-lf', '--lf', help='是否运行上一次失败的用例,1:是、0:否,默认为0', type=str)
    parser.add_argument('-clr', '--clr', help='是否清空已有测试结果,1:是、0:否,默认为0', type=str)
    args = parser.parse_args()

    # 初始化java依赖的libs
    # java_maven_init()
    # # 因为是连跑环境,存在一定可能性需要初始化JAVA的Maven

    # 初始化
    print('%s 开始初始化......' % DateTimeTool.getNowTime())
    frame_logger.info('%s 开始初始化......' % DateTimeTool.getNowTime())
    # api_init() # 因为是连跑环境,存在一定可能性在连跑前重置环境
    print('%s 初始化完成......' % DateTimeTool.getNowTime())
    frame_logger.info('%s 初始化完成......' % DateTimeTool.getNowTime())

    # 执行pytest前的参数准备
    if platform.system() == "Windows":
        pytest_execute_params = ['-c', 'config/pytest.ini', '-r', "3", '-v', '--alluredir', r'.\output\allure_result',
                                 '--clean-alluredir']
    else:
        pytest_execute_params = ['-c', 'config/pytest.ini', '-r', "3", '-v', '--alluredir', r'./output/allure_result',
                                 '--clean-alluredir']

    # 判断目录参数
    dir = 'cases/api/'
    if args.dir:
        dir = args.dir

    # 判断关键字参数
    if args.keyword:
        pytest_execute_params.append('-k')
        pytest_execute_params.append(args.keyword)

    # 判断markexpr参数
    if args.markexpr:
        pytest_execute_params.append('-m')
        pytest_execute_params.append(args.markexpr)

    # 判断是否输出日志
    if args.capture:
        if int(args.capture):
            pytest_execute_params.append('-s')

    # 判断是否失败重跑
    if args.reruns:
        if int(args.reruns):
            pytest_execute_params.append('--reruns')
            pytest_execute_params.append(args.reruns)

    # 判断是否只运行上一次失败的用例
    if args.lf:
        if int(args.lf):
            pytest_execute_params.append('--lf')

    # 判断是否清空已有测试结果
    if args.clr:
        if int(args.clr):
            pytest_execute_params.append('--clean-alluredir')
    pytest_execute_params.append(dir)

    try:
        print('%s开始测试......' % DateTimeTool.getNowTime())
        print("pytest_execute_params", pytest_execute_params)
        # update_environment_info()
        # TODO 连跑完成之后, 看情况决定是否要删除环境信息
        exit_code = pytest.main(pytest_execute_params)
        print("自动化框架连跑结果值exit_code", exit_code)
        print('%s结束测试......' % DateTimeTool.getNowTime())

        eport_data_path = os.path.join(base_path, "output", "allure_result")
        report_path = os.path.join(base_path, "output", "report")
        if platform.system() == "Windows":
            # os.system(f"allure generate {eport_data_path} -o {report_path} --clean")
            os.system(r"allure generate E:\Develop\LoranTest\output\allure_result -o E:\Develop\LoranTest\output\report")
        else:
            # os.system(f"allure generate {eport_data_path} -o {report_path} --clean")
            # 使用定时脚本去跑的时候, 这里可以生成allure_result. 并清除完原目录, 并且此命令对CICD中的操作无影响, 先暂时保留
            os.system(r"cd /usr/local/LoranTest/; allure generate /usr/local/LoranTest/output/allure_result -o /usr/local/LoranTest/output/report --clean")

        # 只在非Window环境才去发生飞书通知
        if platform.system() != "Windows":
            allure_data = AllureFileClean().get_case_count()
            notification_mapping = {
                NotificationType.FEI_SHU.value: FeiShuTalkChatBot(allure_data).post
            }
            notification_mapping.get(notify_config.notify_tool)()

        # 启动服务的步骤, 由定时shell脚本去启动, 这不属于自动化框架

    except Exception as err:
        print("发送飞书通知的时候出现错误err", err)

    if platform.system() == "Windows":
        input("please input any key to exit!")
