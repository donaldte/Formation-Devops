# app/views.py
from django.http import HttpResponse
import os

def server_identity(request):
    webserver = os.environ.get('SERVER_NAME', 'web1')
    return HttpResponse(f"Hello from server {webserver}")
