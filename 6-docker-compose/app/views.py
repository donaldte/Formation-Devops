# app/views.py
from django.http import HttpResponse
import socket
import os


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_container_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)



def server_identity(request):
    webserver = os.environ.get('SERVER_NAME', 'web1')
    dictc={
        'client_ip': get_client_ip(request),
        'container_ip': get_container_ip()
    }
    return HttpResponse(f"Client IP: {dictc['client_ip']}<br>Container IP: {dictc['container_ip']}<br>Webserver: {webserver}")
