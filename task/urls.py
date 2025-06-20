from django.urls import path

from . import views

app_name = 'task'
urlpatterns = [
    path('task/<int:task_id>/change-status/', views.api_change_task_status, name='api_change_task_status'),
    path('subtask/<int:subtask_id>/change-status/', views.api_change_subtask_status,
         name='api_change_subtask_status'),
    path('task/create/', views.task_create, name='task_create'),
    path('task/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_edit'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/<str:slug>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('category/<str:slug>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('category/', views.category_list, name='category_list'),
    path('', views.home, name='home'),
]
