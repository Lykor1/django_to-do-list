from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class TaskLoginView(LoginView):
    template_name = 'account/login.html'

    def form_invalid(self, form):
        messages.error(self.request, _('Неверное имя пользователя или пароль. Пожалуйста, попробуйте снова.'))
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, _(f"Добро пожаловать, {form.get_user().username}!"))
        return super().form_valid(form)


class TaskLogoutView(LogoutView):
    next_page = reverse_lazy('task:home')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Вы вышли из системы.')
        return super().dispatch(request, *args, **kwargs)
