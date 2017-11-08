from django.http import JsonResponse
from sign.models import Event, Guest
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.utils import IntegrityError
import time
# 添加发布会接口
def add_event(request):
    eid = request.POST.get("eid", "")
    name = request.POST.get("name", "")
    limit = request.POST.get("limit", "")
    status = request.POST.get("status", "")
    address = request.POST.get("address", "")
    start_time = request.POST.get("start_time", "")

    if eid == "" or name == '' or limit == '' or address == '' or start_time == '':
        # 将字典转换成Jason格式返回给客户端
        return JsonResponse({'status':10021, 'message':'parameter error'})
    # 查询一下id，如果已存在则返回信息
    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({'status':10022, 'message':'event id already exists'})
    # 查询一下name，如果已存在则返回信息
    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'status':10023,'message':'event name already exists'})

    if status =='':
        status=1

    try:
        Event.objects.create(id=eid, name=name, limit=limit, address=address, status=int(status), start_time=start_time)
    except ValidationError as e:
        error = 'start_time format error. It must be in YYYY-MM-DD HH:MM:SS format.'
        return JsonResponse({'status':10024, 'message':'error'})
    return JsonResponse({'status':200, 'message':'add event success'})

# 查询发布会接口
def get_event_list(request):
    eid = request.POST.get('eid', '')
    name = request.POST.get('name', '')

    if eid == '' and name == '':
        return JsonResponse({'status':10021, 'message':'parameter error'})

    if eid != '':
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status':10022, 'message':'query result is empty'})
        else:
            event['name'] = result.name
            event['address'] = result.address
            event['status'] = result.status
            event['limit'] = result.limit
            event['start_time'] = result.start_time
            return JsonResponse({'status':200, 'message':'success', 'data':event})
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
                 return  JsonResponse({'status':200, 'message':'success', 'data':datas})
         else:
            return JsonResponse({'status':10022, 'message':'query result is empty'})

# 添加嘉宾接口
def add_guest(request):
    eid = request.POST.get('eid', '')
    realname = request.POST.get('realname', '')
    phone = request.POST.get('phone', '')
    email = request.POST.get('email','')

    #如果eid或姓名或电话为空，返回信息
    if eid == '' or realname == '' or phone == '':
        return JsonResponse({'status':10021, 'message':'parameter error'})

    # 如果事件id不存在，返回信息
    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'ststus':10022, 'message':'event id null'})

    # 如果事件状态不可用，返回信息
    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'ststus': 10023, 'message': 'event status is not available'})

    #如果人数超限，返回信息
    event_limit = Event.objects.get(id=eid).limit
    guest_limit = Guest.objects.filter(evnet_id=eid)
    if len(guest_limit) >= event_limit:
        return JsonResponse({'status':10024,'message':'event number is full'})

    event_time = Event.objects.get(id=eid).start_time  # 发布会时间
    print(event_time)
    etime = str(event_time).split(".")[0]
    timeArray = time.strptime(etime, '%Y-%m_%d %H-%M-%S')
    e_time = int(time.mktime(timeArray))

    now_time = str(time.time())   # 当前时间
    ntime = now_time.split('.')[0]
    n_time = int(ntime)

    if n_time >= e_time :
        return JsonResponse({'status':10025, 'message':'event has started'})
    try:
        Guest.objects.create(realname=realname, phone=int(phone), email=email, sign=0, event_id=eid)
    except IntegrityError:
        return JsonResponse({'status':10026, 'message':'the event guest phone number duplicate'})
    return JsonResponse({'status':200, 'message':'add guest success'})

# 嘉宾查询接口
def get_guest_list(request):
    eid = request.GET.get('eid', '')
    phone = request.GET.get('phone', '')

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

        