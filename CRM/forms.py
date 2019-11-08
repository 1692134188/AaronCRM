from django.forms import ModelForm
from django import forms
from CRM import models

#创建一个Form表单需要哪些内容
#1：继承ModelForm
#2：__new__方法：遍历参数，方便前台页面生成控件时，设置class属性
#3：Meta类 主要是配置一些显示、只读属性
#4：clean() 方法 具体某个字段的检查+报错处理、
#5:需要传递两个参数（类，数据）
class EnrollmentForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for filed_name in cls.base_fields:
            filed_obj = cls.base_fields[filed_name]
            filed_obj.widget.attrs.update({'class':'form-control'})
            if filed_name in cls.Meta.readonly_fields:
                filed_obj.widget.attrs.update({'disabled': 'true'})
        return ModelForm.__new__(cls)
    class Meta:
        model=models.StudentEnrollment
        fields="__all__"
        exclude=['contract_approved_date']
        readonly_fields = ['contract_agreed',]

    def clean(self):
        if self.errors:
            return forms.ValidationError(("Please fix errors before re-submit."))
        if self.instance.id is not None:
            for field in self.Meta.readonly_fields:
                old_field_val = getattr(self.instance,field)
                form_val =self.cleaned_data.get(field)
                if old_field_val != form_val:
                    self.add_error(field, "Readonly Field: field should be '{value}' ,not '{new_value}' ". \
                                   format(**{'value': old_field_val, 'new_value': form_val}))


class CustomerForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            filed_obj = cls.base_fields[field_name]
            filed_obj.widget.attrs.update({'class':'form-control'})

            if field_name in cls.Meta.readonly_fields:
                #获取admin中配置的只读字段，生成控件时候设置成disabled
                filed_obj.widget.attrs.update({'disabled': 'true'})
        return ModelForm.__new__(cls)

    class Meta:
        model=models.CustomerInfo
        fields="__all__"
        exclude = ['consult_content', 'status', 'consult_courses']
        readonly_fields = ['contact_type', 'contact', 'consultant', 'referral_from', 'source']

    def clean(self):
        if self.errors: #表单级别的错误
            raise forms.ValidationError(("Please fix errors before re-submit."))

        if self.instance.id is not None:
            #只读字段你，放置某些高手，通过前台页面修改
            for field in self.Meta.readonly_fields:
                old_field_val = getattr(self.instance,field)
                form_val = self.cleaned_data.get(field)
                if old_field_val != form_val:
                    self.add_error(field,"Readonly Field: field should be '{value}' ,not '{new_value}' ".\
                                         format(**{'value':old_field_val,'new_value':form_val}))
