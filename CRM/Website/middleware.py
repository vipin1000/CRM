from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class SessionManagementMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Update last activity timestamp
            request.session['last_activity'] = timezone.now().isoformat()
            
            # Check if session has expired
            last_activity = request.session.get('last_activity')
            if last_activity:
                last_activity = timezone.datetime.fromisoformat(last_activity)
                if (timezone.now() - last_activity).total_seconds() > settings.SESSION_COOKIE_AGE:
                    messages.warning(request, 'Your session has expired. Please log in again.')
                    return redirect('home')

        response = self.get_response(request)
        return response 