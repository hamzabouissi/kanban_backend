from rest_framework import exceptions, status
from rest_framework.views import set_rollback
from django.http import Http404
from django.core.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response


def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'detail': exc.detail}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)
    
    if isinstance(exc, ValidationError):
        data = getattr(exc,"message_dict")
        set_rollback()
        return Response(
            data,
            status=status.HTTP_400_BAD_REQUEST,
        )
    return None


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    return response