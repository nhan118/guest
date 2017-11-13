#!/usr/bin/env python3
#-*- coding:utf-8 -*-
from pymysql import connect, cursors
from pymysql.err import OperationalError
import os
import configparser as cparser

# =========读取db_congig.ini文件设置============
# print("os.path.dirname(__file__) = %s" %os.path.dirname(__file__))
# print(type(os.path.dirname(os.path.dirname(__file__))))
# os.path.dirname(__file__)：获得当前py文件的路径
# os.path.dirname(os.path.dirname(__file__))：获得当前py文件路径的上一级目录，因为db_config.ini文件在这个路径下
base_dir = os.path.dirname(os.path.dirname(__file__))
print(base_dir)
# 转换成windows系统的路径格式
base_dir = base_dir.replace("/", "\\")
print(base_dir)
# 拼接成db_config.ini的完整路径
file_path = base_dir + '\db_config.ini'
print(file_path)

# 1. 创建一个ConfigParser实例
cf = cparser.ConfigParser()
# 2. 读取配置文件
cf.read(file_path)
section = cf.sections()
print(section)
# 读取配置文件的配置项，[]内的是section, 底下的options
host = cf.get("mysqlconf", "host")
port = int(cf.get("mysqlconf", "port"))
db = cf.get("mysqlconf", "db_name")
user = cf.get("mysqlconf", "user")
password = cf.get("mysqlconf", "password")


# ==============封装MYSQL基本操作==============================
# 创建DB类，用于数据库的数据处理
class DB(object):
    def __init__(self):
        '''定义初始化操作'''
        # 连接数据库
        try:
            self.conn = connect(host=host,
                                user=user,
                                password=password,
                                port=port,
                                db=db,
                                charset='utf8mb4',
                                cursorclass=cursors.DictCursor)
        except OperationalError as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    # 清除表数据
    def clear(self, table_name):
        # 1. 先拼出SQL语句的字符串，以下两种清除表的sql语句都可以
        print(table_name)
        real_sql = 'truncate table ' + table_name + ";"
        # real_sql = 'delete from ' + table_name + ";"
        # print(real_sql)
        with self.conn.cursor() as cursor:
            # 禁用表的外键约束，以防止由于外键关联无法删除或更新数据
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(real_sql)
        self.conn.commit()

    # 插入数据
    def insert(self, table_name, table_data):
        # 思路： table_data是一个字典类型，分别读取里面的key和value拼成sql语句，并执行插入
        for key in table_data:
            table_data[key] = "'" + str(table_data[key]) + "'"
            # print(table_data[key])
        key = ','.join(table_data.keys())
        value = ','.join(table_data.values())
        # print(key)
        # print(value)
        real_sql = 'INSERT INTO ' + table_name + " (" + key + ")" + " VALUES " + "(" + value + ")" + ";"
        # print(real_sql)
        # 执行插入
        with self.conn.cursor() as cursor:
            cursor.execute(real_sql)
        self.conn.commit()

    # 关闭数据库连接
    def close(self):
        self.conn.close()

