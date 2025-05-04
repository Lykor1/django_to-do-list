from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from django.utils.timezone import now

from .models import Task, SubTask, Category
from .forms import TaskCreateForm, SubTaskCreateFormSet, TaskFilterForm


def home(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user).prefetch_related('subtasks')
        # if 'category' in request.GET:
        #     category = request.GET['category']
        #     tasks = tasks.filter(category__id=category)
        # else:
        #     category = ''
        # if 'status' in request.GET:
        #     status = request.GET['status']
        #     tasks = tasks.filter(status=status)
        # else:
        #     status = ''
        # filter_form = TaskFilterForm(initial={'category': category, 'status': status})

        category = request.GET.get('category')
        if category and category != '':
            tasks = tasks.filter(category__slug=category)
        status = request.GET.get('status')
        if status and status != '':
            tasks = tasks.filter(status=status)
        initial = {}
        if category:
            initial['category'] = category
        if status:
            initial['status'] = status
        filter_form = TaskFilterForm(initial=initial)
    else:
        tasks = None
        filter_form = None
    context = {
        'tasks': tasks,
        'filter_form': filter_form,
    }
    return render(request, 'task/home.html', context)


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


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        formset = SubTaskCreateFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            task = form.save(commit=False, user=request.user)
            task.save()
            for subtask_form in formset:
                if subtask_form.cleaned_data.get('description'):
                    subtask = subtask_form.save(commit=False, task=task)
                    subtask.save()
            messages.success(request, 'Задача успешно добавлена')
            return redirect('task:home')
        else:
            messages.error(request, 'Ошибка в форме')
    else:
        form = TaskCreateForm()
        formset = SubTaskCreateFormSet()
    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'task/create_task.html', context)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = 'task/task_edit.html'
    success_url = reverse_lazy('task:home')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['subtask_formset'] = SubTaskCreateFormSet(self.request.POST, instance=self.object)
        else:
            context['subtask_formset'] = SubTaskCreateFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        subtask_formset = context['subtask_formset']
        if subtask_formset.is_valid():
            self.object = form.save(commit=False, user=self.request.user)
            self.object.save()
            subtask_formset.instance = self.object
            subtask_formset.save()
            messages.success(self.request, f"Задача '{form.cleaned_data['title']} успешно обновлена!'")
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task:home')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.user
