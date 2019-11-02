from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from KingAdmin import app_setup
from KingAdmin.sites import site
app_setup.kingadmin_auto_discover()


# Create your views here.
def app_index(request):
    return render(request, 'kingadmin/app_index.html', {'site': site})

def get_filter_result(request,querysets):
    filter_conditions={}
    for k,v in request.GET.items():
        if k in ('_page', '_o', '_q'): continue
        if v:
            filter_conditions[k]=v
    return querysets.filter(**filter_conditions),filter_conditions
@login_required
def table_obj_list(request,app_name,model_name):
    # 取出指定model里的数据返回给前端
    admin_class = site.enabled_admins[app_name][model_name]
    querysets = admin_class.model.objects.all()
    # 拿到下拉列表中条件，对数据进行过滤，
    querysets,filter_condtions=get_filter_result(request,querysets)
    # 把条件返回，下拉列表中选中的数据不会丢失
    admin_class.filter_condtions = filter_condtions
    # 获取页数，进行分页处理
    paginator = Paginator(querysets, 5)  # 每页显示5条数据
    page = request.GET.get('_page')
    querysets = paginator.get_page(page)
    return render(request, 'kingadmin/table_obj_list.html', {'querysets': querysets,'admin_class':admin_class,})


def acc_login(request):
    error_msg=""
    if request.method=="POST":
        username=request.POST.get('username')
        password= request.POST.get('password')

        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect(request.GET.get('next', '/kingadmin/'))
        else:
            error_msg = "Wrong username or password!"
    return render(request,"kingadmin/login.html", {'error_msg':error_msg})

def acc_logout(request):
    logout(request)
    return redirect("/kingadmin/login/")