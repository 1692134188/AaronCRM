from django.shortcuts import render

# Create your views here.
def my_courses(request):
    print(request.user.stu_account.profile.enrollment_set.select_related)
    #学生端首页
    return render(request,"stu/my_courses.html")