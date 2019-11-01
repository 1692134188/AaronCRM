from django.db import models

# Create your models here.
class Test(models.Model):
    """测试表"""
    name = models.CharField(max_length=64, unique=True)
    def __str__(self):
        return self.name