import os

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from django.urls import include, path
from rest_framework.request import Request


def ping(request: Request):
    return JsonResponse({'message': 'my message'})


def upload_file(request):
    if request.method == 'POST':
        _type = request.POST['type']
        if _type == 'card_sound':
            pk = request.POST['id']
            _file = request.FILES['file']
            _, ext = os.path.splitext(_file.name)
            save_in_memory_file(_file, f'static/cards/card_{pk}{ext}')

    return JsonResponse({'data': 'success'})


def save_in_memory_file(f: InMemoryUploadedFile, path: str):
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


urlpatterns = [
    path('', include('courses.urls')),
    path('ping/', ping),
    path('auth/', include('lp_auth.urls')),
]
