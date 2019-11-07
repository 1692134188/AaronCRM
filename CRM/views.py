from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from CRM import models
from CRM import forms
from django.utils.timezone import datetime

# Create your views here.

@login_required
def dashboard(request):
    return render(request, 'crm/dashboard.html')


@login_required
def stu_enrollment(request):
    # Q1：此方法的作用是什么？
    #     A1:销售人员为学员分配班级
    customers = models.CustomerInfo.objects.all()
    class_lists = models.ClassList.objects.all()

    if request.method == "POST":
        customer_id = request.POST.get("customer_id")
        class_grade_id = request.POST.get("class_grade_id")
        try:
            enrollment_obj = models.StudentEnrollment.objects.create(
                customer_id=customer_id,
                class_grade_id=class_grade_id,
                consultant_id=request.user.userprofile.id,
            )
        except InterruptedError as e:
            # 已经生成过报名表了
            enrollment_obj = models.StudentEnrollment.objects.get(customer_id=customer_id,
                                                                  class_grade_id=class_grade_id, )
            if enrollment_obj.contract_agreed:
                return redirect("/crm/stu_enrollment/%s/contract_audit/" % enrollment_obj.id)
        enrollment_link = "http://localhost:8000/crm/enrollment/%s/" % enrollment_obj.id

    return render(request, 'crm/stu_enrollment.html', locals())


@login_required
def enrollment(request,enrollment_id):
    # Q1：此方法的作用是什么？
    #     A1:学院在线报名地址
    enrollment_obj = models.StudentEnrollment.objects.get(id=enrollment_id)
    if  enrollment_obj.contract_agreed:
        return HttpResponse("报名合同正在审核中....")

    if request.method == "POST":
        customer_form = forms.CustomerForm(instance=enrollment_obj.customer,data=request.POST)
        if customer_form.is_valid():
            customer_form.save()
            enrollment_obj.contract_agreed=True
            enrollment_obj.contract_signed_date=datetime.now()
            enrollment_obj.save()
            return HttpResponse("您已成功提交报名信息,请等待审核通过,欢迎加入打死都不退费老男孩教育!")

    else:
        customer_form = forms.CustomerForm(instance=enrollment_obj.customer)

    return render(request,"crm/enrollment.html",locals())

