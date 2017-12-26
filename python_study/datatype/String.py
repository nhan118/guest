#!/usr/bin/env python3
#-*- coding:utf-8 -*-

# 单行字符串可使用''或""括起来
# ''''''可以表示多行字符串
str1 = '''这是一个
多行的
字符串
'''
print(str1)

# 字符串的连接，使用“+”
first_name = '韩'
space = ' '
last_name = '宁'
full_name = first_name + space +last_name
print('full name: %s' % full_name)

# 字符串与数字相乘得到N个字符串
print('hello*5 = %s' % ('hello'*5))
# 索引
s = 'hello world'
print('取字符串的第5个字符：%s' % s[4])
print('取字符串的倒数第3个字符：%s' % s[-3])
# 切片有3个参数
# 第一个参数：切片首字符的索引，省略第一个参数表示从头开始取
# 第二个参数：切片结尾字符的索引-1，省略第二个参数表示取到最后一个字符
# 第三个参数：步长，默认是1
print('取字符串的第3至7个字符：%s' % s[2:-2])
# 第一和第二个参数都省略，表示取完整的字符串
print('省略第一和第二个参数s[:]= %s' % s[:])
# 利用切片将字符串逆向输出，步长参数为负值表示倒着取字符串里的字符
# 通常可以用在按创建时间取最新的文件的文件名
print('逆向输出hello worl: %s' % s[::-1])

# 转义字符“\”，用r''括起来的字符串原样输出，不进行转义
print(r'\n没换行，\t没变tab，\\没变"\"')

# 求字符串长度
print('字符串s的长度= %s' % len(s))

# 分割字符串函数split(’分隔符‘)，参数是分隔符，默认值是空格
slist = s.split(' ')
print('分割结果=%s' % slist)

# 连接字符串: sep.join()函数, sep是分隔符，join函数的参数是一个字符串的序列
sep = '~~'
print('连接slist列表中的字符串：%s' % sep.join(slist))

# 字符串转大写s.upper()，得到新串
# 字符串转大写s.lower()，得到新串
print('hello world转大写：%s' % s.upper())

# 替换，返回新串。s.replace(被替换的字符串, 替换成字符串)
print('s中的hello替换成beautiful：%s' % s.replace('hello', 'beautiful'))

# 去除字符串空格：返回新串
# s.strip()：去除两端空格
# s.lstrip()：去除左边空格
# s.rstrip()：去除右边空格
str3 = '   tomorrow is Wednesday   '
print('去掉str3两端空格：%s' % str3.strip())
print('去掉str3左边空格：%s' % str3.lstrip())
print('去掉str3右边空格：%s' % str3.rstrip())

# 强制转换成字符串str()
i = 13910902918
print('将i转换成字符串: %s' % type(str(i)))

# 得到字符的acsii码
print('字符“#”的acsii码是：%s' % ord('#'))

# 得到ascii码代表的字符
print('101代表的字符是：%s' % chr(101))

# 获取用户输入的字符串input()
name = input('你的名字是：')
print("name: %s" % name)