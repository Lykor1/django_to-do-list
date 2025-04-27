from django.urls import path

from . import views

app_name = 'account'
urlpatterns = [
    path('login/', views.TaskLoginView.as_view(), name='login'),
    path('logout/', views.TaskLogoutView.as_view(), name='logout'),
]