from django.shortcuts import render

from .models import Task, SubTask, Category


def home(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user).prefetch_related('subtasks')
    else:
        tasks = None
    context = {
        'tasks': tasks,
    }
    return render(request, 'task/home.html', context)
