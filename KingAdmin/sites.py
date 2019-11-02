# Q1：该文件的作用是什么？
#   A1：将每个模块下的信息注册到全局变量中
from KingAdmin.admin_base import BaseKingAdmin
class AdminSite(object):
    def __init__(self):
        self.enabled_admins={}

    def register(self,model_class,admin_class=None):
        app_name=model_class._meta.app_label #获取模块名称
        model_name = model_class._meta.model_name #获取表名称

        if not admin_class:#为了避免多个model共享一个BaseKingAdmin内存对象
            admin_class=BaseKingAdmin()
        else:
            admin_class =admin_class()
        admin_class.model=model_class
        if app_name not in self.enabled_admins:
            self.enabled_admins[app_name]={}
        self.enabled_admins[app_name][model_name]=admin_class

site=AdminSite()