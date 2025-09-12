from django.contrib import admin
from project.models import *
# Register your models here.

'''class attendanceAdmin(admin.ModelAdmin):
    list_display=('name','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20'
                  '21','22','23','24','25','26','27','28','29','30','31')
admin.site.register(attendance,attendanceAdmin)'''

class studentAdmin(admin.ModelAdmin):
    list_display=('Name','Photo','Class')
admin.site.register(student,studentAdmin)