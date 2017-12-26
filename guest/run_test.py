#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import time, unittest, sys, os
from db_fixture import test_data
from BSTestRunner import BSTestRunner
sys.path.append('..\\interface')

test_dir = './interface'
discover = unittest.defaultTestLoader.discover(test_dir, pattern='*_test.py')

if __name__ == '__main__':
    # 初始化测试数据库
    # print(discover)
    test_data.init_data()
    # 指定测试报告的目录
    report_dir = './report'
    # 获取时间戳
    now = time.strftime('%Y-%m-%d %H_%M_%S')
    # 拼接出完整的路径
    report_name = os.path.join(report_dir, 'Test Report'+now+'.html')
    print('Test start')
    with open(report_name, 'wb') as f:
        runner = BSTestRunner(stream=f, title='Test Report', description='Test add event api')
        runner.run(discover)
    print('Test end')



