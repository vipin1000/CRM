
from .views import *
from django.urls import path


urlpatterns = [
    path('', home, name='home'),
    path('logout/',logout_user,name='logout'),
    path('register/',register_user,name='register'),
    path('add/',add_record,name='add'),
    path('record/<int:pk>',customer_record, name='record'),
    path('del_record/<int:pk>',delete_record, name='delete_record'),
    path('update_record/<int:pk>',update_record, name='update_record'),
    
]