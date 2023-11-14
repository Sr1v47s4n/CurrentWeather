from django.urls import path
from . import views

urlpatterns = [
    path("signup", views.signup, name="signup"),
    path("login_usr", views.login_usr, name="login_usr"),
    path("logout_usr", views.logout_usr, name="logout_usr"),
    path("weather/<int:usrCode>", views.weather, name="weather"),
]
