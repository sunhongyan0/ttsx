from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from hashlib import sha1
import datetime
from .user_login import login_au
from goods.models import GoodsInfo


def login(request):
    name = request.COOKIES.get('name', '')
    context = {'title': '登录', 'name': name, 'top': '0'}
    return render(request, 'dailyfresh/login.html', context)


def login_handle(request):
    post = request.POST
    name = post.get('user_name', '')
    name_jz = post.get('name_jz','0')
    pwd = post.get('pwd', '')
    print(pwd)
    if pwd != '':
        s1 = sha1()
        s1.update(pwd.encode())
        upwd_sha1=s1.hexdigest()
    user = ttsx_info.objects.filter(uname=name)
    context = {'title': '登录', 'name': name, 'pwd': pwd, 'top': '0'}
    if len(user) == 0:
        context['name_error'] = '1'
        return render(request, 'dailyfresh/login.html', context)
    else:
        if user[0].upwd == upwd_sha1:
            request.session['uid'] = user[0].id
            request.session['uname'] = name
            if request.session.has_key('Path'):
                reponse = redirect(request.session['Path'])
            else:
                reponse = redirect('/')
            if name_jz == '1':
                reponse.set_cookie('name', name, expires=datetime.datetime.now() + datetime.timedelta(days = 7))
            else:
                reponse.set_cookie('name', '', max_age=-1)
            return reponse
        else:
            context['pwd_error'] = '1'
            return render(request, 'dailyfresh/login.html', context)


def out(request):
    request.session.flush()
    return redirect('/ttsx/login/')


def register(request):
    context = {'title': '注册', 'top': '0'}
    return render(request, 'dailyfresh/register.html', context)


def register_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    umail = post.get('email')
    s1=sha1()
    s1.update(upwd.encode())
    upwd_sha1=s1.hexdigest()
    user = ttsx_info()
    user.uname = uname
    user.upwd = upwd_sha1
    user.umail = umail
    user.save()
    return redirect('/ttsx/login/')


def register_vaild(request):
    uname = request.GET.get('uname')
    result = ttsx_info.objects.filter(uname=uname).count()
    print(result)
    context = {'valid': result}
    return JsonResponse(context)


@login_au
def user_center_info(request):
    user = ttsx_info.objects.get(pk=request.session['uid'])
    goods_ids = request.COOKIES.get('goods_ids', '').split(',')
    goods_ids.pop()
    glist = []
    for gid in goods_ids:
        glist.append(GoodsInfo.objects.get(id=gid))
    context = {'title': '用户中心', 'user': user, 'show': '1', 'glist': glist}
    return render(request, 'dailyfresh/user_center_info.html', context)


@login_au
def order(request):
    context={'title': '全部订单', 'show': '1'}
    return render(request, 'dailyfresh/user_center_order.html', context)


@login_au
def site(request):
    user = ttsx_info.objects.get(pk=request.session['uid'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uphone = post.get('uphone')
        user.ucode = post.get('ucode')
        user.save()
    context = {'title': '收货地址', 'user': user, 'show': '1'}
    return render(request, 'dailyfresh/user_center_site.html', context)


def islogin(request):
    is_login = 0
    if request.session.has_key('uid'):
        is_login = 1
    return JsonResponse({'is_login': is_login})



