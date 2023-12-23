from django.contrib import admin
from user.models import *


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'description', 'deadline', 'priority', 'done', 'updated_date', 'created_date']
    search_fields = ['user', 'description', 'deadline']
    list_editable = ['description', 'deadline', 'done']

    class Meta:
        model = Task
