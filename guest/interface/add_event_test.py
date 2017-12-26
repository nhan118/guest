#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import unittest
import requests
# import os, sys
from db_fixture import test_data
# parentdir = os.path.dirname(os.path.dirname(__file__))
# parentdir = parentdir.replace("/", "\\")
# sys.path.insert(0, parentdir)
# sys.path.pop(0)

class AddEventTest(unittest.TestCase):
    '''Test add event interface'''
    def setUp(self):
        self.baseurl = 'http://127.0.0.1:8000/api/add_event/'

    def tearDown(self):
        print(self.result)

    def test_add_event_all_null(self):
        '''所有数据为空'''
        param = {'eid':'', 'name':'', 'address':'', 'limit':'', 'start_time':''}
        r = requests.post(self.baseurl, data=param)
        self.result = r.json()
        # 断言结果
        self.assertEqual(self.result['status'], 10021)
        self.assertEqual(self.result['message'], 'parameter error')

    def test_add_event_eid_exist(self):
        '''id已存在'''
        param = {'eid':'1', 'name':'一加5发布会', 'address':'深圳宝体', 'limit':2000, 'start_time':'2017-12-12 10:00:00'}
        r = requests.post(self.baseurl, data=param)
        self.result = r.json()

        self.assertEqual(self.result['status'], 10022)
        self.assertEqual(self.result['message'], 'event id already exists')

    def test_add_event_name_exist(self):
        '''发布会名称已存在'''
        param = {'eid': '11', 'name': '红米pro发布会', 'address': '深圳宝体', 'limit': 2000, 'start_time': '2017-12-12 10:00:00'}
        r = requests.post(self.baseurl, data=param)
        self.result = r.json()

        self.assertEqual(self.result['status'], 10023)
        self.assertEqual(self.result['message'], 'event name already exists')

    def test_add_event_date_type_error(self):
        '''日期格式错误'''
        param = {'eid': '11', 'name': '一加5发布会', 'address': '深圳宝体', 'limit': 2000, 'start_time': '2017'}
        r = requests.post(self.baseurl, data=param)
        self.result = r.json()

        self.assertEqual(self.result['status'], 10024)
        self.assertEqual(self.result['message'], 'start_time format error. It must be in YYYY-MM-DD HH:MM:SS format.')

    def test_add_event_success(self):
        '''添加成功'''
        param = {'eid': '11', 'name': '一加5发布会', 'address': '深圳宝体', 'limit': 2000, 'start_time': '2017-12-12 10:00:00'}
        r = requests.post(self.baseurl, data=param)
        self.result = r.json()

        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'add event success')

if __name__ == '__main__':
    # 初始化数据库
    test_data.init_data()
    unittest.main()

