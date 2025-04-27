from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView
from django.urls import reverse_lazy


class TaskLoginView(LoginView):
    template_name = 'account/login.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Неверное имя пользователя или пароль. Пожалуйста, попробуйте снова.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, f"Добро пожаловать, {form.get_user().username}!")
        return super().form_valid(form)


class TaskLogoutView(LogoutView):
    next_page = reverse_lazy('task:home')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Вы вышли из системы.')
        return super().dispatch(request, *args, **kwargs)


class TaskPasswordChangeView(PasswordChangeView):
    template_name = 'account/password_change_form.html'
    success_url = reverse_lazy('task:home')

    def form_valid(self, form):
        messages.success(self.request, 'Пароль успешно изменён!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Неудача! Проверьте данные!')
        return super().form_invalid(form)


class TaskPasswordResetView(PasswordResetView):
    email_template_name = 'account/password_reset_email.html'
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')

    def form_invalid(self, form):
        messages.error(self.request, 'Неудача! Проверьте адрес электронной почты!')
        return super().form_invalid(form)


class TaskPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class TaskPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:login')

    def form_valid(self, form):
        messages.success(self.request, 'Пароль успешно изменён! Теперь вы можете войти.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Неудача! Проверьте данные!')
        return super().form_invalid(form)
