from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.task_list,name='tasklist'),
    path('task/details/',views.task_detail,name='taskdetails'),
    path('task/create/',views.task_form,name='taskcreate'),
    path('task/update/<int:pk>/', views.task_update, name='task_update'),
    path('task/delete/<int:pk>/', views.task_delete, name='taskdelete'),
]