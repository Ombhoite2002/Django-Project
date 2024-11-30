from django.urls import path,include
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('profile/',views.employeeProfile,name='employeeprofile'),
    path('employee/details/',views.employee_details,name='employeedetails'),
    path('view/employee/profile/<int:employee_id>/', views.view_profile, name="viewprofile"),
    path('tasks/',include('tsmtasks.urls')),
    path('',include('tsmusersdashboards.urls')),
]