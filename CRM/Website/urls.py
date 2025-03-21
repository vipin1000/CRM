
from .views import *
from django.urls import path
urlpatterns = [
    path('', home, name='home'),
    path('logout/',logout_user,name='logout'),
    path('register/',register_user,name='register'),
    path('add/',add_record,name='add'),
    
]