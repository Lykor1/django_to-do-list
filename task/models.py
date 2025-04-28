from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Task(models.Model):
    class Status(models.TextChoices):
        NOT_ACTIVE = 'not_active', 'Не активна'
        ACTIVE = 'active', 'Активна'
        COMPLETED = 'completed', 'Выполнена'

    title = models.CharField(max_length=100, verbose_name='Название задачи')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, allow_unicode=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='tasks')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория', related_name='tasks')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.NOT_ACTIVE,
                              verbose_name='Статус задачи')
    create_date = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')
    due_date = models.DateTimeField(blank=True, null=True, verbose_name='Срок выполнения')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        from django.utils.timezone import now
        return self.due_date < now() if self.due_date else False

    class Meta:
        ordering = ('create_date',)
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        constraints = [
            models.CheckConstraint(
                check=models.Q(due_date__gt=models.F('create_date')),
                name='check_due_date_after_create_date'
            )
        ]


class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks', verbose_name='Задача')
    description = models.TextField(blank=True, verbose_name='Подзадача')
    is_completed = models.BooleanField(default=False, verbose_name='Выполнена')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    completed_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата выполнения')

    def __str__(self):
        return f'{Task.title} - {self.description[:30]}...'

    def save(self, *args, **kwargs):
        if self.is_completed and not self.completed_date:
            from django.utils.timezone import now
            self.completed_date = now()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-create_date', 'task')
        verbose_name = 'Позадача'
        verbose_name_plural = 'Подзадачи'
        default_related_name = 'subtasks'
