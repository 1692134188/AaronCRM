# Q1：该文件的作用是什么？
#     A1：查找当前项目中setting文件中配置的模板。
#         获取每个模块下的kingadmin中的注册信息
#         将注册信息写入到全局变量中

# Q2:如何动态获取配置文件中的内容
#     A2：导入conf文件，conf.settings.INSTALLED_APPS

# Q3：如何将每个模块下的信息注册到全局变量中
#     A3：通过sites.py 方法

from django import conf

def kingadmin_auto_discover():
    mods=conf.settings.INSTALLED_APPS
    for app_name in mods:
        try:
            mod = __import__('%s.kingadmin' % app_name) #动态加载类和函数
        except ImportError:
            pass


