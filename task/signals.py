from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from .models import Category

User = get_user_model()


@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    if created:
        default_categories = [
            'Без категории',
            'Работа',
            'Личное'
        ]
        for category_name in default_categories:
            Category.objects.create(
                user=instance,
                name=category_name,
                slug=slugify(category_name, allow_unicode=True)
            )
