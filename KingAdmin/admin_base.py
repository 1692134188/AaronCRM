class BaseKingAdmin(object):
    list_display=[]  #展示字段
    list_filter=[]   #过滤条件
    search_fields=[] #搜索字段
    list_per_page=3  #显示页码数