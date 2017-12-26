import os
import sys
import django
import django.core.handlers.wsgi

apache_configuration = os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(project)
# 添加setting文件地址
os.environ['DJANGO_SETTINGS_MODULE'] = 'guest.settings'
django.setup()
# 添加项目路径到sys.path
# sys.path.append('D:/Learn/guest')
# sys.path.append('D:/Learn/guest/apache')
application = django.core.handlers.wsgi.WSGIHandler()




