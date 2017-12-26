#!/usr/bin/env python3
#-*- coding:utf-8 -*-
from db_fixture.mysql_db import DB
datas = {'sign_guest':[]}
for i in range(1,3001):
    # 将i转换成字符串
    str_i = str(i)
    realname = 'jack' + str_i
    phone = str(13500110000 + i)
    email = realname + '@mail.com'
    guest = {'realname':realname,'phone':phone, 'email':email, '`sign`':'0', 'event_id':'1'}
    datas['sign_guest'].append(guest)
# print(datas)
def create_guest():
    db = DB()
    for table, data in datas.items():
        db.clear(table)
        for d in data:
            db.insert(table, d)
    db.close()

# 以下是将SQL语句写入文件的办法，但是在sql管理工具里批量执行失败，单句却可以正确执行
# with open('guest.txt','w') as f:
#     for i in range(1,3001):
#         # 将i转换成字符串
#         str_i = str(i)
#         realname = 'jack' + str_i
#         phone = 13500110000 + i
#         email = realname + '@mail.com'
#         sql = 'INSERT INTO sign_guest (realname,phone,email,`sign`,event_id) VALUES ("'+realname+'","'+str(phone)+'","'+email+'","0","1")'
#         # print(sql)
#         f.write(sql)
#         f.write("\n")

if __name__ == '__main__':
   create_guest()