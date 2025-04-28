from django.urls import path

from . import views

app_name = 'account'
urlpatterns = [
    path('login/', views.TaskLoginView.as_view(), name='login'),
    path('logout/', views.TaskLogoutView.as_view(), name='logout'),
    path('password-change/', views.TaskPasswordChangeView.as_view(), name='password_change'),
    path('password-reset/', views.TaskPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.TaskPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', views.TaskPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('register/', views.register, name='register'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/', views.profile, name='profile'),
]
