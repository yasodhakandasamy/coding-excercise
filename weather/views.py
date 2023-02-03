from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import WeatherSerializer, WeatherStatsSerializer
from .paginations import CustomPagination
from .models import Weather, WeatherStats

"""
Create a weather list view allow you to filter the response by fields 
like 'station id' and 'date'. Added custom pagination with page size 10.

"""
class WeatherList(generics.ListAPIView):

    serializer_class = WeatherSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['station_id', 'date']
    search_fields = ['station_id', 'date']
    queryset = Weather.objects.all()

"""
Create a weatherstats list view allow you to filter the response by fields 
like 'station id' and 'year'. Added custom pagination with page size 10.

"""
class WeatherStatsList(generics.ListAPIView):

    serializer_class = WeatherStatsSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    #filter_backends = [filters.SearchFilter]
    filterset_fields = ['station_id', 'year']
    search_fields = ['station_id', 'year']
    queryset = WeatherStats.objects.all()