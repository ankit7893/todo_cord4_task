from django.contrib import admin
from . models import *
# Register your models here.


# admin.site.register(ToDo)

@admin.register(ToDo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('user','name', 'description', 'category', 'status', 'due_date' )



# admin.site.register(TodoShareModal)

@admin.register(TodoShareModal)
class TodoShareModalAdmin(admin.ModelAdmin):
    list_display = ('task','user', 'permission' )

