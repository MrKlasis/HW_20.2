from django.urls import path

from catalog.main.views import index

urlpatterns = [
    path('', index)
]