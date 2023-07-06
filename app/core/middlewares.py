import logging
from django.core.cache import cache
from django.http import JsonResponse
from rest_framework.views import exception_handler
from django.contrib.auth.models import AnonymousUser


def get_user(token):
    user = cache.get(f'user_{cache.get(token)}')
    if user:
        return user
    else:
        return AnonymousUser


class APIAuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        key = request.headers.get("authorization", None)
        if key:
            request.user = get_user(request.headers['authorization'])
        response = self.get_response(request)
        return response


class DisableCSRF(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, "_dont_enforce_csrf_checks", True)
        response = self.get_response(request)

        return response


def core_exception_handler(exc, context):
    print('here')
    response = exception_handler(exc, context)
    if isinstance(exc, Exception):
        print('has exception')
        err_data = {
            'status': False,
            'error': f'{exc.__class__.__name__}: {exc}'
        }
        logging.error(f"Original error detail and call stack: {exc}")
        return JsonResponse(err_data, safe=False, status=503)
    return response