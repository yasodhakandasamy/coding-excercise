from django.urls import path
from .views import WeatherList, WeatherStatsList
from . import views

"""
create url request for weather data 'weather/'
and weather stats 'weather/stats'

"""
urlpatterns = [
    path('weather/', WeatherList.as_view(), name='weather'),
    path('weather/stats/', WeatherStatsList.as_view(), name='weatherstats'),
]