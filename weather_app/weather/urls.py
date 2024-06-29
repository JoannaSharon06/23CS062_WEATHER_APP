from django.urls import path
from . import views
from .views import show_weather

urlpatterns = [
    path('weather/', views.show_weather, name='show_weather'),
]
