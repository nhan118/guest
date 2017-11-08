from django.contrib import admin
from sign.models import Event, Guest
# Register your models here.
# EventAdmin类继承admin.ModelAdmin，admin.ModelAdmin类是一个自定义工具，能够自定义一些模块的特征
class EventAdmin(admin.ModelAdmin):
    # list_display：用于定义显示哪些字段，必须是Event类里定义的字段
    list_display = ['id', 'name', 'status', 'address', 'start_time']
    # 创建搜索栏
    search_fields = ['name']
    # 创建过滤器
    list_filter = ['status']

class GuestAdmin(admin.ModelAdmin):
    list_display = ['realname', 'phone', 'email', 'sign', 'create_time', 'event']
    search_fields = ['realname', 'phone']
    list_filter = ['sign']
admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)

