from django.conf.urls import url
from . import views
urlpatterns=[
    url(r'^order/$', views.order),
    url(r'^site/$', views.site),
    url(r'^register/$', views.register),
    url(r'^user_center_info/$', views.user_center_info),
    url(r'^login/$', views.login),
    url(r'^register_handle/$', views.register_handle),
    url(r'^login_handle/$', views.login_handle),
    url(r'^register_vaild/$', views.register_vaild),
    url(r'^out/$', views.out),
]