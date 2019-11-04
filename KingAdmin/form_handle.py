from django.forms import ModelForm


# Q1：此类的作用是什么？
#     A1：动态生成modelform
def create_dynamic_model_form(admin_class, form_add=False):
    # form_add :Flase修改表单 True添加表单
    class Meta:
        model = admin_class.model
        fields = "__all__"

    def __new__(cls, *args, **kwargs):
        # Q1：此方法的作用是什么？
        #     A1：在生成model_formde的时候给每一个控件添加上一个class
        for field_name in cls.base_fields:
            filed_obj = cls.base_fields[field_name]
            filed_obj.widget.attrs.update({'class': 'form-control'})
        return ModelForm.__new__(cls)

    dynamic_form = type("DynamicModelForm", (ModelForm,), {'Meta': Meta, '__new__': __new__})
    return dynamic_form
