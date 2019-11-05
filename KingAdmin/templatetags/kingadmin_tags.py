from django.template import Library
from django.utils.safestring import mark_safe
import datetime, time

register = Library()

@register.simple_tag
def display_all_related_objs(obj):
    # Q1:此方法的作用是？
    #   A1:数显示要被删除对象的所有关联对象
    ele = "<ul>"
    # 通过a._meta.related_objects可以获取反向关联
    for reversed_fk_obj in obj._meta.related_objects:
        related_table_name = reversed_fk_obj.name
        # 通过表名_set()可以查找所有相关数据
        related_lookup_key = "%s_set" % related_table_name
        related_objs = getattr(obj, related_lookup_key).all()  # 反向查所有关联的数据
        ele += "<li>%s <ul> " % related_table_name

        if reversed_fk_obj.get_internal_type() == "ManyToManyField":  # 不需要深入查找
            for i in related_objs:
                ele += "<li><a href='/kingadmin/%s/%s/%s/change/'>%s</a> 记录里与[%s]相关的的数据将被删除</li>" \
                       % (i._meta.app_label, i._meta.model_name, i.id, i, obj)
        else:
            for i in related_objs:
                # ele += "<li>%s--</li>" %i
                ele += "<li><a href='/kingadmin/%s/%s/%s/change/'>%s</a></li>" % (i._meta.app_label,
                                                                                  i._meta.model_name,
                                                                                  i.id, i)
                ele += display_all_related_objs(i)

        ele += "</ul></li>"

    ele += "</ul>"

    return ele
@register.simple_tag
def build_filter_ele(filter_column, admin_class):
    column_obj = admin_class.model._meta.get_field(filter_column)
    try:
        filter_ele = "<select name='%s'>" % filter_column
        for choice in column_obj.get_choices():
            selected = ''
            if filter_column in admin_class.filter_condtions:  # 当前字段被过滤了
                if str(choice[0]) == admin_class.filter_condtions.get(filter_column):  # 当前值被选中了
                    selected = 'selected'

            option = "<option value='%s' %s>%s</option>" % (choice[0], selected, choice[1])
            filter_ele += option
    except AttributeError as e:
        filter_ele = "<select name='%s__gte'>" % filter_column
        if column_obj.get_internal_type() in ('DateField', 'DateTimeField'):
            time_obj = datetime.datetime.now()
            time_list = [
                ['', '------'],
                [time_obj, 'Today'],
                [time_obj - datetime.timedelta(7), '七天内'],
                [time_obj.replace(day=1), '本月'],
                [time_obj - datetime.timedelta(90), '三个月内'],
                [time_obj.replace(month=1, day=1), 'YearToDay(YTD)'],
                ['', 'ALL'],
            ]

            for i in time_list:
                selected = ''
                time_to_str = '' if not i[0] else "%s-%s-%s" % (i[0].year, i[0].month, i[0].day)
                if "%s__gte" % filter_column in admin_class.filter_condtions:  # 当前字段被过滤了
                    if time_to_str == admin_class.filter_condtions.get("%s__gte" % filter_column):  # 当前值被选中了
                        selected = 'selected'
                option = "<option value='%s' %s>%s</option>" % \
                         (time_to_str, selected, i[1])
                filter_ele += option

    filter_ele += "</select>"
    return mark_safe(filter_ele)

@register.simple_tag
def get_model_name(admin_class):
    return admin_class.model._meta.model_name.upper()

@register.simple_tag
def get_obj_field_val(form_obj,field):
    # Q1:此方法的作用是什么？
    #     A1：在修改页面，将某些无法修改的值转换成label标签
    return getattr(form_obj.instance,field)

@register.simple_tag
def build_table_row(obj, admin_class):
    # Q1:该方法的作用是什么？
    # A1：通过模板，将表中的记录生成相应的html元素
    ele = ""
    if admin_class.list_display:
        for index,column_name in enumerate(admin_class.list_display):
            column_obj = admin_class.model._meta.get_field(column_name)
            if column_obj.choices:
                # 如果是枚举类型，需要将其转换成相应的汉字
                column_date = getattr(obj, 'get_%s_display' % column_name)()
            else:
                column_date = getattr(obj, column_name)
            td_ele = "<td>%s</td>" % column_date
            if index==0:
                td_ele = "<td><a href='%s/change/'>%s</a></td>" % (obj.id,column_date)
            ele += td_ele
    else:
        td_ele = "<td><a href='%s/change/'>%s</a></td>" % (obj.id, obj)
        ele += td_ele
    return mark_safe(ele)

@register.simple_tag
def render_paginator(querysets, admin_class, sorted_column):
    ele = '''
      <ul class="pagination">
    '''
    filter_ele = render_filtered_args(admin_class)
    sorted_ele = ''
    if sorted_column:
        sorted_ele = '&_o=%s' % list(sorted_column.values())[0]
    # 前一页
    if querysets.paginator.page_range and querysets.number and querysets.number > 1:
        p_ele = '''<li class=""><a href="?_page=%s%s%s">%s</a></li>''' % (querysets.number - 1, filter_ele,sorted_ele, '上一页')
        ele += p_ele
    for i in querysets.paginator.page_range:
        if abs(querysets.number - i) < admin_class.list_per_page:  # display btn
            active = ''
            if querysets.number == i:  # current page
                active = 'active'
            p_ele = '''<li class="%s"><a href="?_page=%s%s%s">%s</a></li>''' % (active,i, filter_ele,sorted_ele, i)
            ele += p_ele
    # 后一页
    if querysets.paginator.page_range and querysets.number and querysets.has_next():
        p_ele = '''<li class=""><a href="?_page=%s%s%s">%s</a></li>''' % (querysets.number + 1, filter_ele,sorted_ele, '下一页')
        ele += p_ele
    ele += "</ul>"

    return mark_safe(ele)

@register.simple_tag
def get_sorted_column(column, sorted_column, forloop):
    # Q1:本方法的作用是？
    #     A1:生成url地址栏中的url链接，并处理1：升序降序问题
    if column in sorted_column:
        # 获取上一次排序顺序，本次取反
        last_sort_index = sorted_column[column]
        if last_sort_index.startswith("-"):
            this_time_sort_index = last_sort_index.strip("-")
        else:
            this_time_sort_index = '-%s' % last_sort_index
        return this_time_sort_index
    else:
        return forloop

@register.simple_tag
def render_filtered_args(admin_class,render_html=True):
    # Q1:本方法的作用是？
    #     A1:生成url地址栏中的url链接，保留原始的请求参数
    if  admin_class.filter_condtions:
        ele=''
        for k,v in admin_class.filter_condtions.items():
            ele+='&%s=%s' %(k,v)
        if  render_html:
            return mark_safe(ele)
        else:
            return ele
    else:
        return ''
@register.simple_tag
def render_sorted_arrow(column,sorted_column):
    # Q1:本方法的作用是？
    #     A1:渲染被排序的样式，加个箭头
    if column in sorted_column:
        last_sort_index = sorted_column[column]
        if last_sort_index.startswith('-'):
            arrow_direction = 'bottom'
        else:
            arrow_direction = 'top'
        ele = '''<span class="glyphicon glyphicon-triangle-%s" aria-hidden="true"></span>''' % arrow_direction

        return mark_safe(ele)
    return ''

@register.simple_tag
def get_current_sorted_column_index(sorted_column):
    # Q1:本方法的作用是？
    #     A1:给隐藏域赋值，获取当前的排序字段，以便于过滤的时候保持“排序队形”
    return list(sorted_column.values())[0] if sorted_column else ''

@register.simple_tag
def get_available_m2m_data(field_name,form_obj,admin_class):
    # Q1:本方法的作用是？
    #     A1:给句当前字段名field_name，当前实体form_obj，和admin_class 获取未选中的多对多字段
    field_obj = admin_class.model._meta.get_field(field_name)
    obj_list = set(field_obj.related_model.objects.all())#根据字段名，获取该表中的所有记录
    select_data = []
    try:
        select_data = set(getattr(form_obj.instance,field_name).all())#获取到已经选中的数据
    except:
        pass
    return obj_list-select_data

@register.simple_tag
def get_selected_m2m_data(field_name,form_obj,admin_class):
    # Q1:本方法的作用是？
    #     A1:给句当前字段名field_name，当前实体form_obj，和admin_class 获取已选中的多对多字段
    select_data = set(getattr(form_obj.instance, field_name).all())  # 获取到已经选中的数据
    return select_data

