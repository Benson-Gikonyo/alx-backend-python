from datetime import datetime
from django.utils import timezone
from django.http import JsonResponse
from django.core.cache import cache
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


class OffensiveLanguageMiddleware:

    RATE_LIMIT = 5
    WINDOW_SECONDS = 60

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method.upper() == "POST":
            ip = self.__get__ip(request)
            now = timezone.now()
            key = f"rate:{ip}"

            timestamps = cache.get(key, [])

            cutoff = now.timestamp() - self.WINDOW_SECONDS
            timestamps = [t for t in timestamps if t >= cutoff]

            if len(timestamps) >= self.RATE_LIMIT:
                resp = JsonResponse(
                    {
                        "detail": "Rate limit exceeded. Try again later",
                        "rate limit": self.RATE_LIMIT,
                        "Window_seconds": self.WINDOW_SECONDS,
                    },
                    status=429,
                )
                resp["retry-after"] = str(self.WINDOW_SECONDS)
                return resp

            timestamps.append(now.timestamp())
            cache.set(key, timestamps, timeout=self.WINDOW_SECONDS)

        response = self.get_response
        return response

    def __get__ip(self, request):
        """_Extract client IP, honoring X-Forwarded-For if behind a proxy."""

        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        if xff:
            return xff.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "0.0.0.0")


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if not user.is_authenticated:
            return HttpResponseForbidden("Authentication required")

        user_role = getattr(user, "role", None)

        if user_role not in ("admin", "moderator"):
            if not user.is_staff and not user.is_superuser:
                return HttpResponseForbidden(
                    "You dont have permission to access this resource"
                )

        response = self.get_response
        return response
