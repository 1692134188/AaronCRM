from django.conf.urls import url,include
from CRM import views

urlpatterns = [

    url(r'^$', views.dashboard,name="sales_dashboard"),


]
