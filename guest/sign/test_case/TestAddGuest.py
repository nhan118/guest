#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import base64, json
import unittest
import requests
from Crypto.Cipher import AES


class AddGuestTest(unittest.TestCase):
    def setUp(self):
        # 接口地址
        self.base_url = 'http://127.0.0.1:8086/api/sec_add_guest/'
        # 被加密的字符串长度必须是16的倍数，不足的补上（空格、字符都可以）
        BS = 16
        # 定义一个匿名函数，用于给加密字符串长度补足到16倍数，这里用chr()函数补ascii里的字符
        # 并将这个匿名函数赋值给变量pad，方便调用
        # BS - len(s) % BS ：加密字符串长度除以16求余数，再被16减，得到差几位就满足16的倍数。
        # 余数不会大于16，因此不会出现负值
        # chr()函数返回一个ascii字符，“*”运算符就是得到N个相同的字符
        # 原始字符串 + N个补位的字符 得到一个长度是16倍数的新字符串返回
        self.pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        self.app_key = 'W7v4D60fds2Cmk2U'

    def encryptBase64(self, src):
        # urlsafe是将加密字符里的"+,/"换成"-,_"，避免作为url参数时出错
        return base64.urlsafe_b64encode(src)

    def encryptAES(self, src, key):
        '''生成AES密文'''
        # iv必须是16位
        iv = '1172311105789011'
        # 创建一个AES加密器的实例，传入key，iv以及加密模式参数
        cryptor = AES.new(key, AES.MODE_CBC, iv)
        # 用加密器给要加密的字符串加密，得到一个二进制表示的字符串，很长不便于传输
        ciphertext = cryptor.encrypt(self.pad(src))
        # 对AES加密的字符串用base64进行二次加密，得到一个较短的字符串返回
        return self.encryptBase64(ciphertext)

    def test_add_guest_success(self):
        param = {'eid':'1', 'phone':'13801101112', 'realname':'hans', 'email':'hans@mail.com'}
        # 加密
        encoded = self.encryptAES(json.dumps(param), self.app_key).decode()
        r = requests.post(self.base_url, data={'data':encoded})
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'add guest success')

if __name__ == '__main__':
    unittest.main()