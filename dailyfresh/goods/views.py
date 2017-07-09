from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator

def index(request):
    glist = []
    typeinfo = TypeInfo.objects.all()
    for t in typeinfo:
        nlist = t.goodsinfo_set.order_by('-id')[0:4]
        nclick = t.goodsinfo_set.order_by('-gclick')[0:4]
        glist.append({'t': t, 'nlist': nlist, 'nclick': nclick})
    context = {'title': '首页', 'glist':glist}
    return render(request, 'goods/index.html', context)


def goods_list(request, tid, pindex):
    try:
        print(type(tid))
        t = TypeInfo.objects.get(pk=int(tid))
        new_list = t.goodsinfo_set.order_by('-id')[0:2]
        # 查询当前分类的所有商品，按每页15个来显示
        glist = t.goodsinfo_set.order_by('-id')
        clist = t.goodsinfo_set.order_by('-gclick')
        plist = t.goodsinfo_set.order_by('-gprice')
        paginator = Paginator(glist, 15)
        pindex1 = int(pindex)
        if pindex1 < 1:
            pindex1 = 1
        elif pindex1 > paginator.num_pages:
            pindex1 = paginator.num_pages
        p = paginator.page(pindex1)
        context={'title': '列表', 't': t, 'new_list': new_list,
                 'page': p, 'clist': clist, 'plist': plist}
        return render(request, 'goods/list.html', context)
    except:
        return render(request, '404.html')


def detail(request, id):
    try:
        goods = GoodsInfo.objects.get(pk=int(id))
        goods.gclick += 1
        goods.save()
        new_list = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
        context = {'title': '列表', 'goods': goods, 'new_list': new_list}
        return render(request, 'goods/detail.html', context)
    except Exception as e:
        print(e)
        return render(request, '404.html')
