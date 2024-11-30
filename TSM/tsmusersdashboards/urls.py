from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/panel',views.admin_panel,name='adminpanel'),
    path('employee/dashboard/<int:employee_id>/', views.employee_dashboard, name='employeedashboard'),  
    path('update_task_status/', views.update_task_status, name='update_task_status'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', LogoutView.as_view(next_page='login'), name='employee_logout'),
]