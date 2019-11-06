from django.shortcuts import render
class BaseKingAdmin(object):
    def __init__(self):
        self.action.extend(self.default_action)
    list_display=[]  #展示字段
    list_filter=[]   #过滤条件
    search_fields=[] #搜索字段
    list_per_page=3  #显示页码数
    readonly_fields = []
    filter_horizontal=[]
    default_action =  ['delete_selected_objs']
    action=[]

    def delete_selected_objs(self,request,querysets):
        return render(request, 'kingadmin/table_obj_delete.html')

