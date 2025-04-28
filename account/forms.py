from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password, password_validators_help_text_html


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль', help_text=password_validators_help_text_html)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль')
    email = forms.EmailField(required=True, label='Электронная почта')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Адрес электронной почты обязателен для заполнения.')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот адрес электронной почты уже используется.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('Имя пользователя обязательно для заполнения')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Это имя пользователя уже используется.')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            try:
                validate_password(password, self.instance)
            except forms.ValidationError as error:
                raise forms.ValidationError(error)
        else:
            raise forms.ValidationError('Введите пароль.')
        return password

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if not password2:
            forms.ValidationError('Повторите пароль.')
        elif password != password2:
            raise forms.ValidationError('Пароли не совпадают.')
        return password2
