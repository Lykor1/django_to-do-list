from task.models import Category, Task


def task_context_processor(request):
    context = {
        'categories': Category.objects.all(),
        'statuses': Task.Status.choices,
        'category': '',
        'status': '',
        'all': ''
    }
    # if 'category' in request.GET:
    #     category = request.GET['category']
    #     if category:
    #         context['category'] = f'category={category}'
    #         context['all'] = f"?{context['category']}"
    # if 'status' in request.GET:
    #     status = request.GET['status']
    #     if status:
    #         if context['all']:
    #             context['status'] = f'status={status}'
    #             context['all'] += f"&{context['status']}"
    #         else:
    #             context['status'] = f'status={status}'
    #             context['all'] = f"?{context['status']}"

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
    if query_params:
        context['all'] = f"?{'&'.join(query_params)}"
    return context
