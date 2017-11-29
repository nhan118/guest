#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import requests
import unittest

class UserTest(unittest.TestCase):
    '''用户查询测试'''

    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/users'
        self.auth = ('admin', '1qaz!QAZ')

    def test_user1(self):
        r = requests.get(self.base_url+'/1/', auth=self.auth)
        result = r.json()
        self.assertEqual(result['username'], 'admin')
        self.assertEqual(result['email'], 'themail@sohu.com')

class GroupTest(unittest.TestCase):
    '''用户组查询测试'''

    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/groups'
        self.auth = ('admin', '1qaz!QAZ')

    def test_groups1(self):
        r = requests.get(self.base_url+'/1/', auth=self.auth)
        result = r.json()
        self.assertEqual(result['name'], 'test')

if __name__ == '__main__':
    unittest.main()



