from django.urls import path
from .views import *

app_name = 'student'

urlpatterns = [
    path('degree/', DegreeList.as_view(), name="list_degree"),
    path('degree/create/', DegreeCreate.as_view(), name="add_degree"),
    path('degree/update/<slug>', DegreeUpdate.as_view(), name="update_degree"),
    path('program/', ProgramList.as_view(), name="list_program"),
    path('program/create/', ProgramCreate.as_view(), name="add_program"),
    path('program/update/<slug>', ProgramUpdate.as_view(), name="update_program"),
    #path('student/', StudentList.as_view(), name="list_student"),
    path('student/create/', StudentCreate.as_view(), name="add_student"),
    path('student/update/<pk>', StudentUpdate.as_view(), name="update_student"),
    path('student/delete/<pk>', delete_student,name="delete_student"),
    path('student/profile/<pk>', student_profile, name="student_profile"),

]
