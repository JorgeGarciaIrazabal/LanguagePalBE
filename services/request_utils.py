from django.core.files.uploadedfile import InMemoryUploadedFile

from language_pal_be.authentication import TokenAuthentication


def is_upload_file(func):
    def func_wrapper(request, **kwargs):
        if request.method == 'POST':
            user, token = TokenAuthentication().authenticate(request=request)
            request.user = user
            return func(request, request.FILES['file'], **kwargs)

    return func_wrapper


def save_in_memory_file(f: InMemoryUploadedFile, path: str):
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
