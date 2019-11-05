from KingAdmin import sites
from KingAdmin.sites import site
from KingAdmin.admin_base import BaseKingAdmin
from CRM import models

# Register your models here.
print('crm kingadmin ............')
class CustomerAdmin(BaseKingAdmin):
    list_display = ['id','name','source','contact_type','contact','consultant','consult_content','status','date']
    list_filter = ['source','consultant','status','date']
    search_fields = ['contact','consultant__name']
    list_per_page = 3
    readonly_fields = ['status','contact']

site.register(models.CustomerInfo,CustomerAdmin)
site.register(models.CustomerFollowUp)
# site.register(models.ClassList)
# site.register(models.Course)
# site.register(models.Role)
# site.register(models.Menus)
# site.register(models.CourseRecord)
# site.register(models.StudyRecord)
# site.register(models.Student)
# site.register(models.UserProfile)
