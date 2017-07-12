from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
from datetime import date
from haystack.generic_views import SearchView


def index(request):
    glist = []
    typeinfo = TypeInfo.objects.all()
    for t in typeinfo:
        nlist = t.goodsinfo_set.order_by('-id')[0:4]
        nclick = t.goodsinfo_set.order_by('-gclick')[0:4]
        glist.append({'t': t, 'nlist': nlist, 'nclick': nclick})
    context = {'title': '首页', 'glist':glist}
    return render(request, 'goods/index.html', context)


def goods_list(request, tid, pindex, means):
    try:
        print(type(tid))
        t = TypeInfo.objects.get(pk=int(tid))
        new_list = t.goodsinfo_set.order_by('-id')[0:2]
        # 查询当前分类的所有商品，按每页15个来显示
        # glist = t.goodsinfo_set.order_by('-id')
        # clist = t.goodsinfo_set.order_by('-gclick')
        # plist = t.goodsinfo_set.order_by('-gprice')
        # means = 1
        desc = '1'
        if means == '1':
            glist = t.goodsinfo_set.order_by('-id')
        elif means == '2':
            desc = request.GET.get('desc', '1')
            print(type(desc))
            if desc == '1':
                # desc = '0'
                glist = t.goodsinfo_set.order_by('-gprice')
            else:
                # desc = '1'
                glist = t.goodsinfo_set.order_by('gprice')
        else:
            glist = t.goodsinfo_set.order_by('-gclick')
        paginator = Paginator(glist, 2)
        pindex1 = int(pindex)
        if pindex1 < 1:
            pindex1 = 1
        elif pindex1 > paginator.num_pages:
            pindex1 = paginator.num_pages
        p = paginator.page(pindex1)
        context={'title': '列表', 't': t, 'new_list': new_list,
                 'page': p, 'means': means, 'desc': desc}
        return render(request, 'goods/list.html', context)
    except Exception as e:
        print(e)
        return render(request, '404.html')


def detail(request, id):
    try:
        goods = GoodsInfo.objects.get(pk=int(id))
        goods.gclick += 1
        goods.save()
        new_list = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
        context = {'title': '列表', 'goods': goods, 'new_list': new_list}
        response = render(request, 'goods/detail.html', context)
        goods_ids = request.COOKIES.get('goods_ids', '').split(',')
        print(goods_ids)
        if id in goods_ids:
            goods_ids.remove(id)
        goods_ids.insert(0, id)
        if len(goods_ids) > 6:
            goods_ids.pop()
        goods_ids = ','.join(goods_ids)
        print(goods_ids)
        response.set_cookie('goods_ids', goods_ids, max_age=60*60)
        return response
    except Exception as e:
        print(e)
        return render(request, '404.html')


class MySearchView(SearchView):
    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        context['top'] = '1'
        page_range = []
        page = context.get('page_obj')
        if page.paginator.num_pages <= 5:
            page_range = page.paginator.page_range
        elif page.number <= 2:
            page_range = range(1,6)
        elif page.number >= page.paginator.num_pages:
            page_range = range(page.Paginator.num_pages-4, page.paginator.num_pages+1)
        else:
            page_range = range(page.number-2, page.number+3)
        context['page_range'] = page_range
        return context


