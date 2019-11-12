# 路由配置：
    #1：导包(urls，和views)
from django.conf.urls import url,include
from Student import views

urlpatterns=[
    url(r'^$',views.my_courses,name="my_courses")
]