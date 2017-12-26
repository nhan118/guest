#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import unittest
import requests

class GetEventListTest(unittest.TestCase):
    '''查询发布会信息（带用户认证）'''
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/api/sec_get_event_list/'

    def test_get_event_list_eid_success(self):
        '''根据eid查询结果成功'''
        auth_user = ('admin', '1qaz!QAZ')
        r = requests.post(self.base_url, auth=auth_user, params ={'eid':1})
        result = r.json()
        self.assertEqual(result['status'],200)
        self.assertEqual(result['message'], 'success')
        self.assertEqual(result['data']['name'], u'红米pro发布会')
        self.assertEqual(result['data']['address'], u'北京会展中心')

if __name__ == '__main__':
    unittest.main()