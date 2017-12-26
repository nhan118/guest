#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import json
from django.contrib import auth as django_auth
import base64
import time, hashlib
import requests
from django.db import IntegrityError
from django.http import JsonResponse
from sign.models import Event, Guest
from django.core.exceptions import ObjectDoesNotExist
from Crypto.Cipher import AES
from django.core.exceptions import ValidationError, ObjectDoesNotExist

# 用户认证
def user_auth(request):

    get_http_auth = request.META.get('HTTP_AUTHORIZATION', b'')
    # print(get_http_auth)
    print(request.META)
    auth = get_http_auth.split()
    print(auth)

    try:
        auth_parts = base64.b64decode(auth[1]).decode('utf-8').partition(':')
        print(auth_parts)
    except IndexError:
        return 'null'
    print(auth_parts[0], auth_parts[2])
    username, password = auth_parts[0], auth_parts[2]
    user = django_auth.authenticate(username=username, password=password)
    print(user)
    if user is not None:
        django_auth.login(request, user)
        return 'success'
    else:
        return 'fail'

# 数字签名认证：用户签名+时间戳
def user_sign(request):
    if request.method == 'POST':
        client_time = request.POST.get('time', '')
        client_sign = request.POST.get('sign', '')
    else:
        return 'error'
    if client_sign == '' or client_time == '':
        return 'sign null'

    # 服务器时间
    now_time = time.time()
    # 将得到的浮点数类型的时间转换成字符串，并取小数点之前的部分精度就够了。小数点后是毫秒
    server_time = str(now_time).split('.')[0]

    # 计算时间差
    time_diff = int(server_time) - int(client_time)
    # 如果时间差超过60秒，返回超时错误.
    # 造成时间差有两种可能：
    #   1. 客户端的时间与服务器的时间存在误差超过了60秒，这属于时钟不准。
    #   2. 请求发送到服务器有延迟，延迟时间超过了60秒或者是延迟+时钟误差加在一起超过了60秒
    if time_diff >= 60:
        return 'timeout'

    # 签名检查
    md5 = hashlib.md5()
    # '&Guest-Bugmaster'是客户端秘钥，实际根据接口文档来
    sign_str = client_time + '&Guest-Bugmaster'
    sign_str_utf8 = sign_str.encode(encoding='utf-8')
    print('server: %s' % sign_str_utf8)
    md5.update(sign_str_utf8)
    server_sign = md5.hexdigest()
    print('server sign: %s' % server_sign)

    if server_sign != client_sign:
        return 'sign fail'
    else:
        return 'sign success'

# =========AES加密算法==================
BS = 16
# 还原字符串长度，得到原串
# ord函数是chr函数的配对函数，返回字符对应的10进制数字。
# 这个10进制数字就是补位的位数，利用list切片，获取补位之前的字符串
unpad = lambda s: s[0: - ord(s[-1])]

# 解密base64加密的字符串
def decryptBase64(src):
    return base64.urlsafe_b64decode(src)

# 解密AES密文
def decryptAES(src, key):
    '''解析AES密文'''
    # 和加密的顺序相反，先解密base64的加密
    src = decryptBase64(src)
    iv = '1172311105789011'
    # 创建一个AES对象的实例，传入key，iv以及加密模式
    cryptor = AES.new(key, AES.MODE_CBC, iv)
    # 解密成明文字符串
    text = cryptor.decrypt(src).decode()
    # 去掉补位，返回原串
    return unpad(text)

def aes_encryption(request):
    app_key = 'W7v4D60fds2Cmk2U'
    # 如果请求是POST方法，则获取请求里的data数据。否则返回error
    if request.method == 'POST':
        data = request.POST.get('data', '')
    else:
        return 'error'

    # 解密
    # data就是src，是个json字符串
    decode = decryptAES(data, app_key)
    # 转化为字典
    dict_data = json.loads(decode)
    return dict_data


# 带AES加密认证的查询嘉宾接口
def get_guest_list(request):
    dict_data = aes_encryption(request)
    if dict_data == 'error':
        return JsonResponse({'status':10011, 'message':'request error'})
    # 取出对应发布会的发布会id和嘉宾手机号
    eid = dict_data['eid']
    phone = dict_data['phone']

    #查询嘉宾接口功能
    if eid == '':
        return JsonResponse({'status':10021, 'message':'eid can not be empty'})

    # 如果发布会id不为空而电话为空，则查询出这个发布会的所有嘉宾
    if eid != '' and phone == '':
        datas = []
        results = Guest.objects.filter(event_id=eid)
        if results:
            for r in results:
                guest = {}
                guest['realname'] = results.realname
                guest['phone'] = results.phone
                guest['email'] = results.email
                guest['sign'] = results.sign
                datas.append(guest)
            return JsonResponse({'status':200, 'message':'success', 'data':datas})
        else:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})

    # 如果发布会id和电话都不为空，查询出这个嘉宾
    if eid != '' and phone != '':
        guest = {}
        try:
            result = Guest.objects.get(event_id=eid, phone=phone)
        except ObjectDoesNotExist:
            return JsonResponse({'status':10022, 'message':'guest is not exists'})
        else:
            guest['realname'] = result.realname
            guest['phone'] = result.phone
            guest['email'] = result.email
            guest['sign'] = result.sign
            return JsonResponse({'status':200, 'message':'success', 'data':guest})


# 带用户认证的查询发布会接口
def get_event_list(request):
    auth_result = user_auth(request)
    if auth_result == 'null':
        return JsonResponse({'status':10011, 'message':'user auth null'})
    if auth_result == 'fail':
        return JsonResponse({'status':10012, 'message':'user auth fail'})

    eid = request.GET.get('eid', '')
    name = request.GET.get('name', '')

    if eid == '' and name == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    if eid != '':
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})
        else:
            event['name'] = result.name
            event['address'] = result.address
            event['status'] = result.status
            event['limit'] = result.limit
            event['start_time'] = result.start_time
            return JsonResponse({'status': 200, 'message': 'success', 'data': event})
    if name != '':
        datas = []
        results = Event.objects.filter(name__contains=name)
        if results:
            for r in results:
                event = {}
                event['name'] = r.name
                event['limit'] = r.limit
                event['status'] = r.status
                event['address'] = r.address
                event['start_time'] = r.start_time
                datas.append(event)
                return JsonResponse({'status': 200, 'message': 'success', 'data': datas})
        else:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})

# 添加发布会接口--增加签名+时间戳
def add_event(request):
    sign_result = user_sign(request)
    if sign_result == 'error':
        return JsonResponse({'status':10011, 'message':'request error'})
    elif sign_result == 'sign null':
        return JsonResponse({'status':10012, 'message':'user sign null'})
    elif sign_result == 'timeout':
        return JsonResponse({'status':10013, 'message':'user sign timeout'})
    elif sign_result == 'sign fail':
        return JsonResponse({'status':10014, 'message':'user sign error'})

    # 以下复制add_event的代码即可
    eid = request.POST.get("eid", "")
    name = request.POST.get("name", "")
    limit = request.POST.get("limit", "")
    status = request.POST.get("status", "")
    address = request.POST.get("address", "")
    start_time = request.POST.get("start_time", "")

    if eid == "" or name == '' or limit == '' or address == '' or start_time == '':
        # 将字典转换成Jason格式返回给客户端
        return JsonResponse({'status': 10021, 'message': 'parameter error'})
    # 查询一下id，如果已存在则返回信息
    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({'status': 10022, 'message': 'event id already exists'})
    # 查询一下name，如果已存在则返回信息
    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'status': 10023, 'message': 'event name already exists'})

    if status == '':
        status = 1

    try:
        Event.objects.create(id=eid, name=name, limit=limit, address=address, status=int(status), start_time=start_time)
    except ValidationError as e:
        error = 'start_time format error. It must be in YYYY-MM-DD HH:MM:SS format.'
        return JsonResponse({'status': 10024, 'message': error})
    return JsonResponse({'status': 200, 'message': 'add event success'})

def add_guest(request):
    dict_data = aes_encryption(request)
    if dict_data == 'error':
        return JsonResponse({'status': 10011, 'message': 'request error'})

    # 以下复制add_guest的代码即可
    eid = dict_data['eid']
    realname = dict_data['realname']
    phone = dict_data['phone']
    email = dict_data['email']

    # 如果eid或姓名或电话为空，返回信息
    if eid == '' or realname == '' or phone == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    # 如果事件id不存在，返回信息
    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status': 10022, 'message': 'event id null'})

    # 如果事件状态不可用，返回信息
    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status': 10023, 'message': 'event status is not available'})

    # 如果人数超限，返回信息
    event_limit = Event.objects.get(id=eid).limit
    guest_limit = Guest.objects.filter(event_id=eid)
    if len(guest_limit) >= event_limit:
        return JsonResponse({'status': 10024, 'message': 'event number is full'})

    event_time = Event.objects.get(id=eid).start_time  # 发布会时间
    print(event_time)
    etime = str(event_time).split(".")[0]
    timeArray = time.strptime(etime, '%Y-%m-%d %H:%M:%S')
    e_time = int(time.mktime(timeArray))

    now_time = str(time.time())  # 当前时间
    ntime = now_time.split('.')[0]
    n_time = int(ntime)

    if n_time >= e_time:
        return JsonResponse({'status': 10025, 'message': 'event has started'})
    try:
        Guest.objects.create(realname=realname, phone=int(phone), email=email, sign=0, event_id=eid)
    except IntegrityError:
        return JsonResponse({'status': 10026, 'message': 'the event guest phone number duplicate'})
    return JsonResponse({'status': 200, 'message': 'add guest success'})

def guest_sign(request):
    dict_data = aes_encryption(request)
    if dict_data == 'error':
        return JsonResponse({'status': 10011, 'message': 'request error'})

    # 以下复制user_sign的代码即可
    eid = dict_data['eid']
    phone = dict_data['phone']
    print('eid=%s\nphone=%s' % (eid, phone))
    # 如果event id或手机号为空，返回错误信息
    if eid == '' or phone == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    # 如果查不到给定的event id的发布会，返回错误信息
    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status': 10022, 'message': 'event id null'})

    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status': 10023, 'message': 'event status is not available'})

    event_time = Event.objects.get(id=eid).start_time
    etime = str(event_time).split('.')[0]
    timeArray = time.strptime(etime, '%Y-%m-%d %H-%M-%S')
    e_time = int(time.mktime(timeArray))

    now_time = str(time.time())
    ntime = now_time.split('.')[0]
    n_time = int(ntime)

    # 如果当前时间>=发布会开始时间，返回错误信息
    if n_time >= e_time:
        return JsonResponse({'status': 10024, 'message': 'event has started'})

    # 如果查不到给出的手机号，返回错误信息
    result = Guest.objects.filter(phone=phone)
    if not result:
        return JsonResponse({'status': 10025, 'message': 'user phone null'})

    # 如果按照发布会id和手机号没查到结果，返回错误信息
    result = Guest.objects.filter(id=eid, phone=phone)
    if not result:
        return JsonResponse({'status': 10026, 'message': 'user did not participate in the conference'})

    result = Guest.objects.get(id=eid, phone=phone).sign
    if result:
        return JsonResponse({'status': 10027, 'message': 'user has sign in'})
    else:
        Guest.objects.filter(id=eid, phone=phone).update(sign='1')
        return JsonResponse({'status': 200, 'message': 'sign success'})
if __name__ == '__main__':
    base_url = 'http://127.0.0.1:8000/api/sec_get_event_list/'



