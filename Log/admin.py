from django.contrib import admin
from . models import *
# Register your models here.


# admin.site.register(TaskLog)
@admin.register(TaskLog)
class TaskLogAdmin(admin.ModelAdmin):
    list_display = ('task','user','name', 'description', 'category', 'status', 'due_date', 'change_date', 'result_status' )

