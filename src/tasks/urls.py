from django.urls import path
from .views import task_list, complete_task, delete_task, register_user, login_view, logout_view

urlpatterns = [
    path('', task_list, name='task_list'),
    path('complete/<int:pk>/', complete_task, name='complete_task'),
    path('delete/<int:pk>/', delete_task, name='delete_task'),
    path('register/', register_user, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout')
]
