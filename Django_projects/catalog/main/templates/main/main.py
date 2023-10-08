from django.shortcuts import render
from django.urls import path
from django.conf import settings
from django.core.management import execute_from_command_line
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
                'DIRS': [os.path.join(BASE_DIR, 'templates')],
                'APP_DIRS': True,
            },
        ],
    )
    execute_from_command_line(["manage.py", "runserver"])
