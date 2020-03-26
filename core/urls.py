from django.urls import path
from .views import *
from student.views import StudentCreate

app_name = 'core'

urlpatterns = [
    path('login/', login, name='login'),
    path('', StudentCreate.as_view(), name='dashboard'),
    path('logout/', logout, name='logout'),
    path('change-my-password/', change_my_password, name='change_my_password'),
    path('groups/', list_groups, name='list_groups'),
    path('groups/create/', add_group, name='add_group'),
    path('groups/update/<pk>', update_group, name='update_group'),
    # path('groups/delete/<pk>', views.delete_group, name='delete_group'),
    path('admin-user/', list_users, name='list_users'),
    path('admin-user/create/', create_user, name='create_user'),
    path('admin-user/update/<int:id>', update_user, name='update_user'),
    path('admin-user/delete/<int:id>', delete_user, name='delete_user'),
    path('admin-user/change-password/<int:id>', change_password_user, name='change_password_user'),
    path('unauthorized', unauthorized, name='unauthorized'),
]
