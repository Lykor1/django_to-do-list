from django.urls import path

from . import views

app_name = 'task'
urlpatterns = [
    path('api/task/<int:task_id>/change-status/', views.api_change_task_status, name='api_change_task_status'),
    path('api/subtask/<int:subtask_id>/change-status/', views.api_change_subtask_status,
         name='api_change_subtask_status'),
    path('', views.home, name='home'),
]
