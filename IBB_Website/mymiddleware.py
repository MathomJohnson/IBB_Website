from django.shortcuts import redirect
from django.http import Http404

class AdminRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') and (not request.user.is_staff or not request.user.is_authenticated):
            raise Http404
        
        if request.path.startswith('/calendar/google-login') and (not request.user.is_staff or not request.user.is_authenticated):
            raise Http404
        
        return self.get_response(request)