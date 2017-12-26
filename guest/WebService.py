#!/usr/bin/env python3
#-*- coding:utf-8 -*-
from suds.client import Client
from xml.parsers.expat import ParserCreate
from suds.xsd.doctor import ImportDoctor, Import

# 电话号码归属地查询
url = 'http://ws.webxml.com.cn/WebServices/MobileCodeWS.asmx?wsdl'
client = Client(url)
print(client)
result = client.service.getMobileCodeInfo('18518917687')
# print(result)

# 天气查询
# url = 'http://ws.webxml.com.cn/WebServices/WeatherWebService.asmx?wsdl'
# imp = Import('http://www.w3.org/2001/XMLSchema', location='http://www.w3.org/2001/XMLSchema.xsd')
# imp.filter.add('http://WebXml.com.cn/')
# d = ImportDoctor(imp)
# client = Client(url, doctor=d)
# print(client)
# result = client.service.getWeatherbyCityName("杭州")
# print(result)

