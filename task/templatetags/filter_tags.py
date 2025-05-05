from django import template
from django.urls import reverse
from urllib.parse import urlencode

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace_param(context, **kwargs):
    request = context['request']
    dict_ = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            dict_[key] = value
        else:
            if key in dict_:
                del dict_[key]
    url = reverse('task:home')
    encoded_params = urlencode({k: v for k, v in dict_.items() if v}, doseq=True)
    if encoded_params:
        return f'{url}?{encoded_params}'
    return url
