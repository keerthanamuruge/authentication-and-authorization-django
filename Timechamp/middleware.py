from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotAuthenticated
from rest_framework.views import exception_handler
import logging
from django.http import JsonResponse
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from authentication.views import RegisterView, LoginView

logger = logging.getLogger(__name__)

handler400 = 'rest_framework.exceptions.bad_request'


def get_response(exc):
    if exc:
        if hasattr(exc, 'default_detail'):
            return {"error": {exc.default_code: exc.default_detail,
                              }, "status_code": exc.status_code
                    }
        else:
            return {"error": str(exc), "status_code": exc.status_code  if hasattr(exc, 'status_code') else 400}


def handle_exception(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.

    handlers = {'ValidationError': _handle_validate_generic_error, 'PermissionDenied': _handle_generic_error,
                }
    response = exception_handler(exc, context)

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        handlers[exception_class](exc, context, response)
        return response
    response.data = get_response(exc)
    logger.exception(exc)
    return response


def _handle_generic_error(exception, context, response):
    response.data = get_response(exception)
    logger.warning(exception)
    return response.data


def _handle_validate_generic_error(exception, context, response):
    response.data = {"error": {exception.default_code: exception.detail,
                              }, "status_code": exception.status_code
                    }
    return response.data


class TokenValidator:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if hasattr(view_func, 'cls'):
            if not view_func.cls == RegisterView or view_func.cls == LoginView:
                jwt_auth = JWTAuthentication()
                try:
                    user, payload = jwt_auth.authenticate(request)
                    user.payload = payload
                    request.user = user
                except TypeError:
                    response = get_response(exc=NotAuthenticated())
                except AuthenticationFailed:
                    response = get_response(exc=AuthenticationFailed())
                except Exception:
                    response = get_response(get_response(Exception))

                return JsonResponse(response, status=response['status_code'])

    # def process_exception(self, request, exception):  #     h(exception, request.context)

    # def process_template_response(self, request, response):  #     response.context_data['new_data'] = self.context_response
