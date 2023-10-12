#!/usr/bin/venv python
"""Django's command-line utility for administrative tasks."""
import sys
import os
from django.shortcuts import render
from django.urls import path
from django.conf import settings
from django.core.management import execute_from_command_line




def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

SE_DIR = os.path.dirname(os.path.abspath(__file__))

def home(request):
    return render(request, 'home.html')

def contacts(request):
    return render(request, 'contacts.html')

urlpatterns = [
    path('', home, name='home'),
    path('contacts', contacts, name='contacts'),
]

if __name__ == '__main__':
    settings.configure(
        DEBUG=True,
        ROOT_URLCONF=__name__,
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join(SE_DIR, 'templates')],
                'APP_DIRS': True,
            },
        ],
    )
    execute_from_command_line(["manage.py", "runserver"])

