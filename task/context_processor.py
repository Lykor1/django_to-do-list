from django.contrib.auth.models import AnonymousUser

from task.models import Category, Task


def task_context_processor(request):
    context = {
        'categories': [],
        'statuses': Task.Status.choices,
        'category': '',
        'status': '',
        'search': '',
        'page': '',
        'all': ''
    }
    if request.user and not isinstance(request.user, AnonymousUser):
        context['categories'] = Category.objects.filter(user=request.user)

    query_params = []
    if 'category' in request.GET:
        category = request.GET['category']
        if category:
            context['category'] = f'category={category}'
            query_params.append(context['category'])
    if 'status' in request.GET:
        status = request.GET['status']
        if status:
            context['status'] = f'status={status}'
            query_params.append(context['status'])
    if 'search' in request.GET:
        search = request.GET['search']
        if search:
            context['search'] = f'search={search}'
            query_params.append(context['search'])
    if 'page' in request.GET:
        page=request.GET['page']
        if page:
            context['page'] = f'page={page}'
            query_params.append(context['page'])
    if query_params:
        context['all'] = f"?{'&'.join(query_params)}"
    return context
