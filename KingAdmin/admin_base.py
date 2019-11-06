from django.shortcuts import render
import json
class BaseKingAdmin(object):
    def __init__(self):
        self.actions.extend(self.default_actions)

    list_display=[]  #展示字段
    list_filter=[]   #过滤条件
    search_fields=[] #搜索字段
    list_per_page=3  #显示页码数
    readonly_fields = []
    filter_horizontal=[]
    default_actions = ['delete_selected_objs']
    actions = []

    def delete_selected_objs(self,request,querysets):
        querysets_ids = json.dumps([i.id for i in querysets])
        return render(request, 'kingadmin/table_obj_delete.html',{'admin_class':self,"objs":querysets,"querysets_ids":querysets_ids})

