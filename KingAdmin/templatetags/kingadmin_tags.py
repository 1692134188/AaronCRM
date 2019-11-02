from django.template import Library
from django.utils.safestring import mark_safe
register = Library()

@register.simple_tag
def build_table_row(obj, admin_class):
    # Q1:该方法的作用是什么？
    # A1：通过模板，将表中的记录生成相应的html元素
    ele = ""
    for column_name in admin_class.list_display:
        column_obj = admin_class.model._meta.get_field(column_name)
        if column_obj.choices:
            # 如果是枚举类型，需要将其转换成相应的汉字
            column_date = getattr(obj,'get_%s_display' %column_name)()
        else:
            column_date = getattr(obj, column_name)
        td_ele = "<td>%s</td>" % column_date
        ele += td_ele
    return mark_safe(ele)
