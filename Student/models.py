from django.db import models

from CRM.models import User,UserProfile,CustomerInfo

# Create your models here.
class Account(models.Model):
    account = models.OneToOneField(User,related_name="stu_account",on_delete=None)
    profile = models.OneToOneField(CustomerInfo,on_delete=None)