from django.urls import path
from . import views

urlpatterns = [
    path("", views.apicall),
    path("search", views.apicall),
]


