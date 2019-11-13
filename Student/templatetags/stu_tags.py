# 定义模板三要素：
    #1：导入
from django.template import Library

register = Library()

@register.simple_tag()
def test(request):
    pass
