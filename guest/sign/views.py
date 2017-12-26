from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.db.models import Q # 用于filter中的“或”条件
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # 用于分页显示数据
from django.shortcuts import render, get_object_or_404  # 用于签到页面
from django.db.models import Count  # 用于对嘉宾计数
# Create your views here.
def index(request):
    return render(request, "index.html")

#登录动作
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)  # 登录
            response = HttpResponseRedirect('/event_manage/')
            # response.set_cookie('user', username, 3600) # 添加浏览器cookie
            request.session['user'] = username  # 将session信息记录到浏览器
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})
# 发布会管理
@login_required  # 装饰器，用于设置成功页必须登录才能访问
def event_manage(request):
    # username = request.COOKIES.get('user', '') # 读取浏览器cookie
    # 获取所有发布会的数据
    event_list = Event.objects.all()
    username = request.session.get('user', '')  # 读取浏览器session
    return render(request, 'event_manage.html', {'user': username, 'events': event_list})

# 发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user":username, "events":event_list})

# 嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 100, 2)  # 创建分页器，每页3条数据,少于2条将合并到上一页
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整数，取第一页面数据
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果page不在范围，取最后一页面
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'guest_manage.html',{'user':username, 'guests':contacts})

# 姓名、电话搜索
@login_required
def search_name_phone(request):
    username = request.session.get('user', '')  # 获取当前session里的user
    search_name_phone = request.GET.get("name_phone", "")  # 获取用户的查询字符串，参数名为输入框控件的name属性值
    # 用查询字符串分别在realname和phone字段查询，是或的关系。Q()内输入查询子句
    guest_list = Guest.objects.filter(Q(realname__contains=search_name_phone)|Q(phone__contains=search_name_phone))
    return render(request, "guest_manage.html", {"user":username, "guests":guest_list})

# 签到页面
@login_required
def sign_index(request, eid):
    # 从页面URL获得一个event.id，然后依据此id从事件库中获取这个事件，如果不存在就抛出http404错误
    event = get_object_or_404(Event, id=eid)
    guests = calc_guest(eid)
    total = guests[0]
    signed = guests[1]
    unsigned = guests[2]
    return render(request, 'sign_index.html', {"event":event, "total":total, 'signed':signed, 'unsigned':unsigned})

# 签到动作
@login_required
def sign_index_action(request, eid):
    # 根据url中的eid，获取当前事件
    event = get_object_or_404(Event, id=eid)
    # 获取url中的手机号
    phone = request.POST.get("phone", "")
    print(phone)
    # 调用calc_guest(eid)函数，得到发布会签到人数情况
    guests = calc_guest(eid)
    total = guests[0]
    signed = guests[1]
    unsigned = guests[2]
    # 判断手机号是否存在，如果不存在就显示错误提示
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {"event":event, "hint":"phone error.", "total":total, 'signed':signed, 'unsigned':unsigned})
    # 判断手机号和事件id是否存在，如果不存在就显示错误提示
    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign_index.html', {"event":event, "hint":"event id or phone error.", "total":total, 'signed':signed, 'unsigned':unsigned})
    # 判断来宾是否已经签到，显示相应的提示
    # 注意！这里一定不能用filter方法，filter方法返回的是一个集合，不是一个对象。返回对象要用get
    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, 'sign_index.html', {"event":event, "hint":"user has sign in.", "total":total, 'signed':signed, 'unsigned':unsigned})
    else:
        # 更新数据库中的sign字段，标记为已签到
        # 注意！更新数据库时，必须用filter方法，是对QuerySet集合操作，不能用get方法
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        # 调用calc_guest(eid)函数，得到发布会签到人数情况
        # 此分支人数发生了变化，需要重新查询一遍
        guests = calc_guest(eid)
        total = guests[0]
        signed = guests[1]
        unsigned = guests[2]
        return render(request, 'sign_index.html', {"event":event, "hint":"sign in  success.", "guest":result, "total":total, 'signed':signed, 'unsigned':unsigned})

# 退出登录
@login_required
def logout(request):
    auth.logout(request)  # 退出登录
    response = HttpResponseRedirect('/index/')
    return response
# 签到人数计算
def calc_guest(eid):
    guest_count = Guest.objects.filter(event_id=eid).values("event_id").annotate(count=Count("event_id")).values(
        "event_id", "count")
    # guest_count是一个结果集[{'event_id':1,'count':5}]
    # 是列表里包个字典，取列表的第1个元素，key='count'的值
    total = guest_count[0]['count']
    # 查询已经签到的嘉宾，得到一个嘉宾列表结果集
    guest_signed = Guest.objects.filter(event_id=eid, sign='1')
    # 求结果集列表的长度，即可得知有几个人签到
    signed = len(guest_signed)
    # 总人数减已经签到的人数，得到未签到人数
    unsigned = int(total) - signed
    return (int(total), signed, unsigned)