from KingAdmin import sites
from KingAdmin.sites import site
from CRM import models

# Register your models here.
print('crm kingadmin ............')
class CustomerAdmin(sites.AdminSite):
    list_display = ['name','source','contact_type','contact','consultant','consult_content','status','date']
    list_filter = ['source','consultant','status','date']
    search_fields = ['contact','consultant__name']

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