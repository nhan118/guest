#!/usr/bin/env python3
#-*- coding:utf-8 -*-
from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode
from spyne.server.wsgi import WsgiApplication
from spyne.protocol.soap import Soap11
from wsgiref.simple_server import make_server
import sys
sys.path.append('')

class HelloWorldService(ServiceBase):
    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(ctx, name, times):
        for i in range(times):
            yield  'Hello, %s' % name
application = Application([HelloWorldService],
        tns = 'spyne.examples.hello',
        in_protocol = Soap11(validator='lxml'),
        out_protocol = Soap11()
                          )
if __name__ == '__main__':
    wsgi_app = WsgiApplication(application)
    server = make_server('127.0.0.1', 8001, wsgi_app)
    server.serve_forever()