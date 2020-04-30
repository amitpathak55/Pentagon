from django.urls import path
from .views import *
from student.views import StudentList

app_name = 'core'

urlpatterns = [
    path('login/', login, name='login'),
    path('', StudentList.as_view(), name='dashboard'),
    path('logout/', logout, name='logout'),
]
