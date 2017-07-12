from django.conf.urls import url
from . import views
urlpatterns = [
    url('^add/$', views.add),
    url('^count/$', views.count),
    url('^$', views.index),
]