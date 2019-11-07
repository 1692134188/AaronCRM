from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import  login_required
from CRM import models

# Create your views here.

@login_required
def dashboard(request):

    return render(request, 'crm/dashboard.html')

@login_required
def stu_enrollment(request):
    # Q1：此方法的作用是什么？
    customers = models.CustomerInfo.objects.all()
    class_lists = models.ClassList.objects.all()

    if  request.method == "POST":
        customer_id = request.POST.get("customer_id")
        class_grade_id=request.POST.get("class_grade_id")
        try:
            enrollment_obj = models.StudentEnrollment.objects.create(
                customer_id = customer_id,
                class_grade_id=class_grade_id,
                consultant_id=request.user.userprofile.id,
            )
        except InterruptedError as e:
            #已经生成过报名表了
            enrollment_obj=models.StudentEnrollment.objects.get(customer_id=customer_id,class_grade_id=class_grade_id,)
            if enrollment_obj.contract_agreed:
                return redirect("/crm/stu_enrollment/%s/contract_audit/" % enrollment_obj.id)
        enrollment_link = "http://localhost:8000/crm/enrollment/%s/" %enrollment_obj.id

    return render(request, 'crm/stu_enrollment.html',locals())
