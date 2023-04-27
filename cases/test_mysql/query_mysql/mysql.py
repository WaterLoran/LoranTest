# -*- coding: utf-8 -*-
import logging
import pymysql
import sys
from core.logger import logger_init, logger_end
import os
from core.logger import get_logger


class Mysql(object):
    def __init__(self):
        self.db = None
        pass

    def get_server_ip_port(self):
        mysql_ip = "127.0.0.1"
        mysql_port = 3306
        return mysql_ip, mysql_port

    def get_mysql_password(self):
        """
        实际运行时,需要在pycharm中设置环境变量,如果实在Linux中运行的时候,也要相对应去设置
        :return:
        """
        mysql_password = os.getenv('MYSQL_PWD')
        if not mysql_password:
            print("请先将MYSQL数据库的密码设置到环境变量中")
            print("mysql_password", mysql_password)
            assert False
        return mysql_password

    def mysqladmin_flush_hosts(self):
        pass

    def connect_to_mysql(self):
        mysql_ip, mysql_port = self.get_server_ip_port()
        mysql_password = self.get_mysql_password()
        # print(mysql_ip, mysql_port)
        # print(mysql_password)
        db = pymysql.connect(
            host=mysql_ip,
            port=mysql_port,
            user='root',
            passwd=mysql_password,
            db='master_mysql',
            charset='utf8'
        )
        self.db = db

    def exec_sql(self, sql=""):
        if sql == "":
            assert False

        if self.db is None:
            self.connect_to_mysql()
        db = self.db

        cursor = db.cursor()
        result = None
        try:
            cursor.execute(sql)  # 执行sql语句
            result = cursor.fetchall()  # 返回数据库查询的所有信息，用元组显示
            db.commit()  # COMMIT命令用于把事务所做的修改保存到数据库
        except Exception as err:
            db.rollback()  # 发生错误时回滚
            logging.error("exec_sql_cmd:exec cmd failed, err:{}".format(err))
        cursor.close()  # 关闭游标
        return result

    def change_database(self, target_databases="master_mysql"):
        sql = "use {};".format(target_databases)
        logging.info("change_databases::sql ==> {}".format(sql))
        self.exec_sql(sql=sql)

    def exec_sql_in_database(self, database="master_mysql", sql=""):
        self.change_database(target_databases=database)
        res = self.exec_sql(sql=sql)
        return res

def exec_sql(sql):
    logger = get_logger()

    print("\nsql命令 => ", sql)
    logger.info("\nsql命令 => " + sql)

    tool = Mysql()
    res = tool.exec_sql(sql)
    logger.info("res是 => " + str(res))
    print("res是 => ", res)
    print("\n")

    # 如果需要从获取调用栈信息,参考下面的代码
    # last_func = sys._getframe(1).f_code.co_filename
