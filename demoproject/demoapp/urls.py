
from django.urls import path
from . import views

urlpatterns = [
    path('', views.demohome,name='demohome'),
    path('<int:photo_id>/',views.img_info,name='img_info')
]