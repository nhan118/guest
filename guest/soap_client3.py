#!/usr/bin/env python3
#-*- coding:utf-8 -*-
from suds.client import Client

url = 'http://127.0.0.1:8001/?wsdl'
client = Client(url)
result = client.service.say_hello("bugmaster", 3)
print(result)