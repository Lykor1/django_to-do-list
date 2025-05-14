from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import UpdateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import now
from urllib.parse import urlencode

from .models import Task, SubTask, Category
from .forms import TaskCreateForm, SubTaskCreateFormSet, TaskFilterForm, CategoryCreateForm


def home(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user).prefetch_related('subtasks')

        category = request.GET.get('category')
        if category and category != '':
            tasks = tasks.filter(category__slug=category)
        status = request.GET.get('status')
        if status and status != '':
            tasks = tasks.filter(status=status)
        search = request.GET.get('search')
        if search and search != '':
            tasks = tasks.filter(Q(title__icontains=search))

        initial = {}
        if category:
            initial['category'] = category
        if status:
            initial['status'] = status
        if search:
            initial['search'] = search

        filter_form = TaskFilterForm(initial=initial)

        page_size = 5
        paginator = Paginator(tasks, page_size)
        page_number = request.GET.get('page')
        try:
            page_number = int(page_number) if page_number else 1
            page_obj = paginator.get_page(page_number)
        except (ValueError, EmptyPage, PageNotAnInteger):
            page_obj = paginator.page(1)
    else:
        page_obj = None
        filter_form = None
    context = {
        'page_obj': page_obj,
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
                    'completed_date': subtask.completed_date.isoformat() if subtask.completed_date else None
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
                             'completed_date': subtask.completed_date.isoformat() if subtask.completed_date else None
                             })
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskCreateForm(request.user, request.POST)
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
        form = TaskCreateForm(request.user)
        formset = SubTaskCreateFormSet()
    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'task/create_task.html', context)


class RedirectToFilteredListMixin:
    def get_success_url(self):
        current_filters = self.request.GET.copy()
        home_url = reverse('task:home')
        encoded_filters = urlencode(current_filters)
        if encoded_filters:
            redirect_url = f'{home_url}?{encoded_filters}'
        else:
            redirect_url = home_url
        return redirect_url


class TaskUpdateView(RedirectToFilteredListMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = 'task/task_edit.html'

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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
            messages.success(self.request, f"Задача '{form.cleaned_data['title']}' успешно обновлена!")
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class TaskDeleteView(RedirectToFilteredListMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.user

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Задача была удалена')
        return response


@login_required
def category_list(request):
    return render(request, 'task/category_list.html')


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryCreateForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False, user=request.user)
            category.save()
            messages.success(request, f"Категория '{form.cleaned_data['name']}' успешно добавлена")
            return redirect('task:category_list')
        else:
            messages.error(request, 'Ошибка. Проверьте данные')
    else:
        form = CategoryCreateForm()
    return render(request, 'task/category_create.html', {'form': form})


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'task/category_edit.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        category = self.get_object()
        return self.request.user == category.user

    def get_object(self, queryset=None):
        return get_object_or_404(Category, slug=self.kwargs['slug'], user=self.request.user)

    def form_valid(self, form):
        self.object = form.save(commit=False, user=self.request.user)
        self.object.save()
        messages.success(self.request, f"Категория '{form.cleaned_data['name']}' успешно обновлена")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task:category_list')


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        category = self.get_object()
        return self.request.user == category.user

    def get_object(self, queryset=None):
        return get_object_or_404(Category, slug=self.kwargs['slug'], user=self.request.user)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, f"Категория '{self.object.name}' была удалена")
        return response

    def get_success_url(self):
        return reverse('task:category_list')
