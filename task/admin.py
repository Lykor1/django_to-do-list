from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Task, SubTask


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1
    fields = ('description', 'is_completed', 'create_date', 'completed_date')
    readonly_fields = ('create_date', 'completed_date')


UserAdmin.search_fields = ('username', 'email', 'first_name', 'last_name')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'status', 'create_date', 'due_date')
    list_filter = ('status', 'category', 'create_date')
    search_fields = ('title', 'user__username', 'category__name')
    list_editable = ('status',)
    date_hierarchy = 'create_date'
    readonly_fields = ('create_date',)
    autocomplete_fields = ('user',)
    inlines = [SubTaskInline]
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'user', 'category', 'status')
        }),
        ('Даты', {
            'fields': ('create_date', 'due_date'),
            'classes': ('collapse',)
        }),
    )
