#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import unittest
import time, hashlib
import requests

class AddEventTest(unittest.TestCase):
    '''带数字签名认证的添加发布会接口测试'''

    def setUp(self):
        # 接口地址
        self.base_url = 'http://127.0.0.1:8000/api/sec_add_event/'
        # 秘钥
        self.api_key = '&Guest-Bugmaster'
        # 当前时间
        now_time = time.time()
        self.client_time = str(now_time).split('.')[0]
        # 数字签名
        md5 = hashlib.md5()
        # 签名前的字符串
        sign_str = self.client_time + self.api_key
        # 把字符串用UTF8编码
        sign_str_utf8 = sign_str.encode(encoding='utf-8')
        print('test client: %s' % sign_str_utf8)
        # 对字符串加密
        md5.update(sign_str_utf8)
        # 得到签名后的字符串
        self.sign_md5 = md5.hexdigest()
        print('client md5: %s' % self.sign_md5)

    def test_add_event_time_out(self):
        '''请求超时'''
        now_time = str(int(self.client_time) - 60)
        param = {'eid':'', 'name':'', 'limit':'', 'address':'', 'start_time':'',
                 'time':now_time, 'sign':self.sign_md5}
        r = requests.post(self.base_url, data=param)
        result = r.json()
        print(result)
        self.assertEqual(result['status'], 10013)
        # self.assertEqual(result['message'], 'user sign null')

if __name__ == '__main__':
    unittest.main()



