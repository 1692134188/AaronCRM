from django.forms import ModelForm
from django import forms
from CRM import models

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
