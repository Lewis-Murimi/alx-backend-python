# chats/middleware.py

import logging
import threading
from collections import defaultdict
from datetime import datetime, timedelta

from django.http import HttpResponseForbidden, JsonResponse


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger("request_logger")
        handler = logging.FileHandler("requests.log")
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)
        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current hour (24hr format)
        current_hour = datetime.now().hour

        # Deny access outside 18 (6PM) and 21 (9PM)
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden("Access to chat is restricted during this time.")

        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_counts = defaultdict(list)
        self.lock = threading.Lock()

    def __call__(self, request):
        # Only track POST requests to /messages/ endpoint (i.e., sending messages)
        if request.method == 'POST' and '/messages' in request.path:
            ip = self.get_client_ip(request)
            now = datetime.now()

            with self.lock:
                # Remove timestamps older than 1 minute
                self.message_counts[ip] = [
                    timestamp for timestamp in self.message_counts[ip]
                    if now - timestamp < timedelta(minutes=1)
                ]

                if len(self.message_counts[ip]) >= 5:
                    return HttpResponseForbidden("Rate limit exceeded: Only 5 messages per minute allowed.")

                # Record the current message
                self.message_counts[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only apply to specific restricted endpoints, e.g. message creation/deletion
        restricted_paths = ["/api/messages/", "/api/conversations/"]
        restricted_methods = ["POST", "PUT", "DELETE"]

        if request.path in restricted_paths and request.method in restricted_methods:
            if not request.user.is_authenticated:
                return JsonResponse({"error": "Authentication required"}, status=401)

            user_role = getattr(request.user, 'role', None)
            if user_role not in ['admin', 'moderator']:
                return JsonResponse({"error": "Forbidden: insufficient role permissions"}, status=403)

        return self.get_response(request)
