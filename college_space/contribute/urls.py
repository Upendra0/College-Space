from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.contribute, name='contribute'),
]
