#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import Guest, Event
# class UserSeriaLizer(serializers.HyperlinkedModelSerializer):
    # 示例代码
    # class Meta:
    #     model = User
    #     fields = ('url', 'username', 'email', 'groups')

# class GroupSerializer(serializers.HyperlinkedModelSerializer):
    # 示例代码
    # class Meta:
    #     model = Group
    #     fields = ('url', 'name')

class EventSerialLizer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model =Event
       fields = ('url', 'name', 'address', 'status', 'start_time', 'limit')

class GuestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Guest
        fields = ('url', 'realname', 'phone', 'email', 'sign', 'event')



