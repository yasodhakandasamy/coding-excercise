from .models import Weather, WeatherStats
from rest_framework import serializers

"""serializer for weather model"""
class WeatherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Weather
        fields = "__all__"

"""serializer for weather stats model"""
class WeatherStatsSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = WeatherStats
        fields = "__all__"