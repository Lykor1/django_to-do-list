from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


def get_declension(number, one, few, many):
    """
    Возврат правильной формы в зависимости от числа
    """
    num_str = str(number)
    last_digit = int(num_str[-1])
    if len(num_str) > 1:
        last_two_digits = int(num_str[-2:])
    else:
        last_two_digits = last_digit
    if 11 <= last_two_digits <= 14:
        return many
    elif last_digit == 1:
        return one
    elif 2 <= last_digit <= 4:
        return few
    else:
        return many


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=50, db_index=True, allow_unicode=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='categories')

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='tasks')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория', related_name='tasks')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.NOT_ACTIVE,
                              verbose_name='Статус задачи')
    create_date = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')
    due_date = models.DateTimeField(blank=True, null=True, verbose_name='Срок выполнения')

    def __str__(self):
        return self.title

    def get_relative_due_date(self):
        """
        Возвращает относительный срок выполнения задачи (например, "завтра", "через 2 дня", "через 5 минут").
        """
        if not self.due_date:
            return ""
        now = timezone.now()
        if self.due_date < now:
            return "(просрочено)"
        time_difference: timedelta = self.due_date - now
        total_seconds = int(time_difference.total_seconds())
        if total_seconds < 60:
            return "(менее минуты)"
        minutes = total_seconds // 60
        hours = total_seconds // 3600
        days = time_difference.days
        now_localized = timezone.localtime(now)
        due_date_localized = timezone.localtime(self.due_date)
        tomorrow_start = now_localized.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        day_after_tomorrow_start = tomorrow_start + timedelta(days=1)
        if tomorrow_start <= due_date_localized < day_after_tomorrow_start:
            return "(завтра)"
        if days > 0:
            day_word = get_declension(days, "день", "дня", "дней")
            return f"(через {days} {day_word})"
        elif hours > 0:
            hour_word = get_declension(hours, "час", "часа", "часов")
            return f"(через {hours} {hour_word})"
        elif minutes > 0:
            minute_word = get_declension(minutes, "минуту", "минуты", "минут")
            return f"(через {minutes} {minute_word})"
        else:
            return "(менее минуты)"

    @property
    def is_overdue(self):
        from django.utils.timezone import now
        return self.due_date < now() if self.due_date else False

    class Meta:
        ordering = ('-create_date',)
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
        ordering = ('create_date',)
        verbose_name = 'Позадача'
        verbose_name_plural = 'Подзадачи'
        default_related_name = 'subtasks'
