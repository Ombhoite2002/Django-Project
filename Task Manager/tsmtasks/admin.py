from django.contrib import admin
from .models import Task
from django.db import models

# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'priority', 'due_date', 'status', 'created_at')  # Fields displayed in the list view
    list_filter = ('priority', 'due_date', 'status')  # Add filters for priority, due_date, and status
    search_fields = ('task_name', 'task_description')  # Enable search by task name and description
    ordering = ('-created_at',)  # Default ordering by created_at in descending order
    readonly_fields = ('created_at', 'updated_at')  # Fields to make read-only
    
    # Customize form to use a select dropdown for assigned employee (since ForeignKey is used)
    fieldsets = (
        (None, {
            'fields': ('task_name', 'task_description', 'assigned_employees', 'priority', 'due_date', 'status')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    # You can also specify specific widgets for fields if needed (e.g., for date fields)
    formfield_overrides = {
        models.DateField: {'widget': admin.widgets.AdminDateWidget()},
    }

admin.site.register(Task, TaskAdmin)
