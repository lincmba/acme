# Create your views here.
from django.shortcuts import render
from django_eventstream import get_current_event_id


def stream_import(request, task_id=None):
    context = {}
    context['url'] = f'/events/{task_id}'
    context['last_id'] = get_current_event_id([task_id])
    return render(request, 'products/track_import_progress.html', context)
