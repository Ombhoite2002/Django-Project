from django.contrib import admin
from .models import Employee,EmployeeProfile

# Register your models here.

class EmployeeProfileInline(admin.StackedInline):
    model = EmployeeProfile
    extra = 0 

class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('employee', 'first_name', 'last_name', 'role', 'phone_number')
    search_fields = ('employee__username', 'first_name', 'last_name', 'role', 'phone_number')
    list_filter = ('gender', 'role')
    ordering = ('employee',)

admin.site.register(EmployeeProfile, EmployeeProfileAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    inlines = [EmployeeProfileInline]
    list_display = ('username', 'email')
    search_fields = ('username', 'email')

admin.site.register(Employee, EmployeeAdmin)

