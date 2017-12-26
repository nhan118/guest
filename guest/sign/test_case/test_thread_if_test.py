#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import threading
from time import time
import requests
import json
import unittest
import base64
from Crypto.Cipher import AES

class TestUserSignPerf(unittest.TestCase):
    '''Performance test of user sign'''
    def setUp(self):
        # 定义接口的基本地址
        self.base_url = 'http://192.168.1.104:8086/api/user_sign/'


    # def test_sign(self):
    #     param = {'eid':1, 'phone':13500110013}
    #     r = requests.post(self.base_url, data=param)
    #     self.result = r.json()
    #     self.assertEqual(self.result['status'], 200)

    # 签到线程，线程要做的事情
    def sign_thread(self, start_user, end_user):
        for i in range(start_user, end_user):
            phone = 13500110000 + i
            datas = {"eid":1, "phone":phone}
            r = requests.post(self.base_url + "/api/user_sign/", data=datas)
            self.result = r.json()
            try:
                self.assertEqual(self.result['status'], 200)
                self.assertEqual(self.result['message'], 'sign success')
            except AssertionError as e:
                print("phone:" + str(phone) + ", user sign fail!")
    def test_user_sign(self):
        # 设置用户分组，分成5组即5个线程
        lists = {1: 601, 601: 1201, 1201: 1801, 1801: 2401, 2401: 3001}
        # 创建线程数组
        threads = []
        # 创建线程
        for start_user, end_user in lists.items():
            t = threading.Thread(target=self.sign_thread, args=(start_user, end_user))
            threads.append(t)

        # 开始时间
        start_time = time()

        # 启动线程
        for i in range(len(lists)):
            threads[i].start()
        for i in range(len(lists)):
            threads[i].join()

        # 结束时间
        end_time = time()

        print("start_time:" + str(start_time))
        print("end time:" + str(end_time))
        print("run time:" + str(end_time - start_time))


if __name__ == '__main__':
    unittest.main()
