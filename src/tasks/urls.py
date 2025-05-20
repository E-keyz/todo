from django.urls import path
from .views import task_list, complete_task, delete_task, register_user, login_view, logout_view, dashboard, edit_task, toggle_complete

urlpatterns = [
    path('tasks/', task_list, name='task_list'),
    path('complete/<int:task_id>/', complete_task, name='complete_task'),
    path('delete/<int:task_id>/', delete_task, name='delete_task'),
    path('register/', register_user, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', dashboard, name='dashboard'),
    path('edit/<int:task_id>/', edit_task, name='edit_task'),
    path('toggle/<int:task_id>/', toggle_complete, name='toggle_complete'),

]
