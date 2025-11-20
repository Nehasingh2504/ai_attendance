from django.contrib import admin
from home.models import *

class studentAdmin(admin.ModelAdmin):
    list_display=('Name','Photo','Class')
admin.site.register(student,studentAdmin)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['name'] + [f'day_{i}' for i in range(1, 32)]
    list_editable = [f'day_{i}' for i in range(1, 32)]
    list_display_links = ['name']