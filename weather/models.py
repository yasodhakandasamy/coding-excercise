from django.db import models

"""create weather model for weather data"""
class Weather(models.Model):
    station_id = models.CharField(primary_key=True,max_length=20)
    date = models.DateField()
    max_temp = models.IntegerField() #maximum temperature
    min_temp = models.IntegerField() #minimum temperature
    rain = models.IntegerField() #amount of precipitation

    class Meta:
        db_table = 'weather_data'

"""create weatherstats model for weather_stats data"""
class WeatherStats(models.Model):
    station_id = models.CharField(primary_key=True, max_length=20)
    year = models.IntegerField()
    avg_min_temp = models.DecimalField(decimal_places=2,max_digits=8) #Average minimum temperature
    avg_max_temp = models.DecimalField(decimal_places=2,max_digits=8) #Average maximum temperature
    total_rain = models.DecimalField(decimal_places=2,max_digits=8) #Total accumulated precipitation

    class Meta:
        db_table = 'weather_stats'