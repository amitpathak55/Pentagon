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
    path('student/', StudentList.as_view(), name="list_student"),
    path('student/create/', StudentCreate.as_view(), name="add_student"),
    path('student/update/<pk>', StudentUpdate.as_view(), name="update_student"),
    path('student/education-history/<pk>', education_history, name="list_education_history"),
    path('student/education-history/<pk>/create', create_education_history, name="create_education_history"),
    path('student/education-history/<pk>/update', update_education_history, name="update_education_history"),
    path('student/education-history/<pk>/delete', delete_education_history, name="delete_education_history"),
    path('student/files/<pk>', list_user_files, name="list_user_files"),
    path('student/files/<pk>/upload', upload_user_file, name="upload_user_file"),
    path('student/files/<pk>/delete', delete_user_file, name="delete_user_file"),
    path('student/notes/<pk>', list_user_notes, name="list_user_notes"),
    path('student/notes/<pk>/create', add_user_note, name="add_user_note"),
    path('student/notes/<pk>/update', update_user_note, name="update_user_note"),
    path('student/notes/<pk>/delete', delete_user_note, name="delete_user_note"),
    path('student/employment-history/<pk>', list_user_employment_history, name="list_user_employment_history"),
    path('student/employment-history/<pk>/create', add_employment_history, name="add_employment_history"),
    path('student/employment-history/<pk>/update', update_employment_history, name="update_employment_history"),
    path('student/employment-history/<pk>/delete', delete_employment_history, name="delete_employment_history"),

]