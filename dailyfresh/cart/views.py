from django.shortcuts import render
from django.http import JsonResponse
from goods.models import GoodsInfo
from .models import *
from django.db.models import Sum


def add(request):
    try:
        uid = request.session.get('uid')
        gid = int(request.GET.get('gid'))
        count = int(request.GET.get('count', '1'))
        carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
        if len(carts):
            cart = carts[0]
            cart.user_id = uid
            cart.goods_id = gid
            cart.count += count
            cart.save()
        else:
            cart = CartInfo()
            cart.user_id = uid
            cart.goods_id = gid
            cart.count = count
            cart.save()
        return JsonResponse({'isadd': 1})
    except:
        return JsonResponse({'isadd': 0})


def count(request):
    uid = request.session.get('uid')
    # cart_count = CartInfo.objects.filter(user_id=uid).count()
    cart_count = CartInfo.objects.filter(user_id=uid).aggregate(Sum('count')).get('count__sum')
    return JsonResponse({'count': cart_count})


def index(request):
    uid = request.session.get('uid')
    cart_list = CartInfo.objects.filter(user_id=uid)
    context = {'title': '购物车', 'cart_list': cart_list}
    return render(request, 'cart/cart.html', context)

