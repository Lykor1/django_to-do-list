from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import UserRegistrationForm, ProfileEditForm


class TaskLoginView(LoginView):
    template_name = 'account/login.html'

    def form_valid(self, form):
        messages.success(self.request, f"Добро пожаловать, {form.get_user().username}!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Проверьте адрес электронной почты и пароль.')
        return super().form_invalid(form)


class TaskLogoutView(LogoutView):
    next_page = reverse_lazy('task:home')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Вы вышли из системы.')
        return super().dispatch(request, *args, **kwargs)


class TaskPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'account/password_change_form.html'
    success_url = reverse_lazy('task:home')
    login_url = reverse_lazy('account:login')

    def form_valid(self, form):
        messages.success(self.request, 'Пароль успешно изменён!')
        return super().form_valid(form)


class TaskPasswordResetView(PasswordResetView):
    email_template_name = 'account/password_reset_email.html'
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')


class TaskPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class TaskPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:login')

    def form_valid(self, form):
        messages.success(self.request, 'Пароль успешно изменён! Теперь вы можете войти.')
        return super().form_valid(form)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            messages.success(request, f'Вы зарегистрированы как {user_form.cleaned_data["username"]}!')
            return redirect('account:login')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def profile(request):
    user = request.user
    return render(request, 'account/profile.html', {'user': user})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профиль успешно изменён!')
            return redirect('account:profile')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'account/profile_edit.html', {'form': form})

@login_required
def profile_delete(request):
    if request.method == 'POST':
        try:
            user = request.user
            user.delete()
            logout(request)
            messages.success(request, 'Ваш профиль был удален.')
            return redirect(reverse_lazy('task:home'))
        except Exception as e:
            messages.error(request, f'Произошла ошибка при удалении профиля: {e}')
            return redirect('account:profile')

    else:
        return redirect('account:profile')
