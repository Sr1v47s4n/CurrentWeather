from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from .models import User, City
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
import requests

@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def signup(request):
    if request.method == "POST":
        userName = request.POST.get("userName")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        emailAddress = request.POST.get("emailAddress")
        fullName = request.POST.get("fullName")
        try:
            if password1 != password2:
                messages.error(
                    request, "Password and Confirmation Password does not match."
                )
                return redirect('signup')
            else:
                if User.objects.get(userName=userName):
                    messages.error(request, "Username already exists")
                    return redirect('signup')
        except User.DoesNotExist:
            user = User(
                userName=userName,
                password=make_password(password1),
                emailAddress=emailAddress,
                fullName=fullName,
                is_superuser=False,
                is_staff=False,
                is_active=True,
                usrCode=usr_code(),
            )
            user.save()
            return redirect("weather", user.usrCode)

    return render(request, "webusr/signup.html")


def logout_usr(request):
    logout(request)
    return redirect("login_usr")

@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def login_usr(request):
    if request.method == "POST":
        userName = request.POST.get("userName")
        password = request.POST.get("password")
        try:
            user = User.objects.get(userName=userName)
            user = authenticate(userName=userName, password=password)
            if user is not None:
                login(request, user)
                print(user.usrCode)
                return redirect("weather", user.usrCode)
            else:
                messages.error(request, "Password Not Matched")
                return redirect('login_usr')
        except User.DoesNotExist:
            messages.error(request, "User Not Found")
            return redirect('login_usr')

    return render(request, "webusr/login.html")


@login_required(login_url="login_usr")
def weather(request, usrCode):
    api_call = "http://api.openweathermap.org/data/2.5/weather?q={}&units={}&appid=877579016703840e7a5a4cd773efc9df"
    cities = City.objects.filter(usrCode=usrCode)
    user = User.objects.get(usrCode=usrCode)
    unit = "metric"
    if request.method == "POST":
        city_name = request.POST.get("city_name")
        if city_name is not None:
            new_city = City(usrCode=user.usrCode, city=city_name)
            new_city.save()
        del_city = request.POST.get("del_city")
        if del_city is not None:
            dlt_city = City.objects.get(id=del_city)
            dlt_city.delete()
        unit = request.POST.get("unit")
    if request.method == "GET":
        pass
    cities_data = []
    try:

        for city in cities:
            city_weather = requests.get(api_call.format(city.city, unit)).json()
            data = {
                "name": city.city.capitalize(),
                "temp": city_weather["main"]["temp"],
                "desc": city_weather["weather"][0]["description"].capitalize(),
                "icon": city_weather["weather"][0]["icon"],
                "unit": "°C" if unit == "metric" else "°F",
                "id": city.id,
            }
            cities_data.append(data)
    except KeyError:
        pass
    context = {"cities_data": cities_data, "usrCode": usrCode}
    return render(request, "webusr/Current-Weather.html", context)


def usr_code():
    import random
    import math

    def code_creater():
        ls = [i for i in range(0, 10)]
        num_6 = ""
        for i in range(6):
            index = math.floor(random.random() * 10)
            num_6 += str(ls[index])
        return num_6

    def is_unique():
        code = code_creater()
        try:
            WebUsr = User.objects.get(usrCode=code)
        except User.DoesNotExist:
            return code

    return is_unique()
