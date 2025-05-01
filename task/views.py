from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

from .models import Task, SubTask, Category


@login_required
def api_change_task_status(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, user=request.user)
        status_order = [Task.Status.NOT_ACTIVE, Task.Status.ACTIVE, Task.Status.COMPLETED]
        current_index = status_order.index(task.status)
        next_index = (current_index + 1) % len(status_order)
        task.status = status_order[next_index]

        subtask_updates = []
        if task.status == Task.Status.COMPLETED:
            subtasks = task.subtasks.filter(is_completed=False)
            for subtask in subtasks:
                subtask.is_completed = True
                subtask.completed_date = now()
                subtask.save()
                subtask_updates.append({
                    'id': subtask.id,
                    'is_completed': subtask.is_completed,
                    'completed_date': subtask.completed_date.strftime(
                        '%d.%m.%Y %H:%M') if subtask.completed_date else None
                })

        task.save()
        return JsonResponse({'status': 'success', 'new_status': task.status, 'subtask_updates': subtask_updates})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required
def api_change_subtask_status(request, subtask_id):
    if request.method == 'POST':
        subtask = get_object_or_404(SubTask, id=subtask_id, task__user=request.user)
        subtask.is_completed = not subtask.is_completed
        if subtask.is_completed and not subtask.completed_date:
            subtask.completed_date = now()
        elif not subtask.is_completed:
            subtask.completed_date = None
        subtask.save()
        return JsonResponse({'status': 'success',
                             'is_completed': subtask.is_completed,
                             'completed_date': subtask.completed_date.strftime(
                                 '%d.%m.%Y %H:%M') if subtask.completed_date else None})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def home(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user).prefetch_related('subtasks')
    else:
        tasks = None
    context = {
        'tasks': tasks,
    }
    return render(request, 'task/home.html', context)
