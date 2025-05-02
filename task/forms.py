from django import forms
from django.utils.timezone import now

from .models import Task, SubTask, Category


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'category', 'status', 'due_date')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название задачи'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local', 'placeholder': 'дд.мм.гггг чч:мм'},
                format='%Y-%m-%dT%H:%M')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = None
        try:
            default_category = Category.objects.get(name='Без категории')
            self.fields['category'].initial = default_category
        except Category.DoesNotExist:
            pass
        self.fields['status'].initial = Task.Status.NOT_ACTIVE

    def save(self, commit=False, user=None):
        instance = super().save(commit=False)
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance


class SubTaskCreateForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ('description', 'is_completed')
        widgets = {
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 1, 'placeholder': 'Введите описание подзадачи'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def save(self, commit=False, task=None):
        instance = super().save(commit=False)
        if task:
            instance.task = task
        instance.create_date = now()
        if instance.is_completed and not instance.completed_date:
            instance.completed_date = now()
        elif not instance.is_completed:
            instance.completed_date = None
        if commit:
            instance.save()
        return instance


SubTaskCreateFormSet = forms.inlineformset_factory(Task, SubTask, form=SubTaskCreateForm,
                                                   fields=('description', 'is_completed'),
                                                   extra=1, can_delete=True)
