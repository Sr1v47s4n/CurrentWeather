from django.shortcuts import render
import requests

# Create your views here.


def apicall(request):
    fapi_call = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=877579016703840e7a5a4cd773efc9df"
    capi_call = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=877579016703840e7a5a4cd773efc9df"
    city = "Chennai"
    if request.method == "POST":
        city = request.POST.get("city_name")
    if request.method == "GET":
        pass
    city_weather = requests.get(capi_call.format(city)).json()
    fcity_weather = requests.get(fapi_call.format(city)).json()
    data = {
        "city": city.capitalize(),
        "ctemp": city_weather["main"]["temp"],
        "ftemp": fcity_weather["main"]["temp"],
        "desc": city_weather["weather"][0]["description"].capitalize(),
        "icon": city_weather["weather"][0]["icon"],
    }
    context = {"data": data}
    return render(request, "webapp/Current-Weather.html", context)

def page_not_found_view(request, exception):
    return render(request, "error/404.html", status=404)


def server_error(request):
    return render(request, "error/500.html", status=500)
