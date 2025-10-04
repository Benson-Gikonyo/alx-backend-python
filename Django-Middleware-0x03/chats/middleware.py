from datetime import datetime
import logging
from django.http import HttpResponseForbidden


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        logging.basicConfig(
            filename="requests.log", level=logging.INFO, format="%(message)s"
        )

    def __call__(self, request):
        response = self.get_response(request)

        user = request.user.username if request.user.is_authenticated else "Anonymous"

        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)

        response = self.get_response(request)

        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().hour

        if current_time < 18 and current_time >= 21:
            return HttpResponseForbidden("Access denied during this time.")

        response = self.get_response(request)
        return response
