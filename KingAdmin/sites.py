# Q1：该文件的作用是什么？
#   A1：将每个模块下的信息注册到全局变量中

class AdminSite(object):
    def __init__(self):
        self.enabled_admins={}

    def register(self,model_class,admin_class=None):
        app_name=model_class._meta.app_label #获取模块名称
        model_name = model_class._meta.model_name #获取表名称
        if app_name not in self.enabled_admins:
            self.enabled_admins[app_name]={}
        self.enabled_admins[app_name][model_name]=admin_class

site=AdminSite()