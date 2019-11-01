from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from KingAdmin import app_setup
from KingAdmin.sites import site
app_setup.kingadmin_auto_discover()

def app_index(request):
    return render(request, 'kingadmin/app_index.html', {'site': site})
# Create your views here.
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