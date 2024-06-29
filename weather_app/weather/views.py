from django.shortcuts import render
import requests
from datetime import datetime
from django.contrib import messages

def time_format_for_location(utc_with_tz):
    local_time = datetime.utcfromtimestamp(utc_with_tz)
    return local_time.strftime("%H:%M:%S")

def get_weather_data(city_name):
    api_key = "784877c279c12a49b6f96a31d1ec4b09"
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
    response = requests.get(weather_url)
    return response.json() if response.status_code == 200 else None

def show_weather(request):
    weather_data = None
    if request.method == 'POST':
        city_name = request.POST.get('city')
        weather_info = get_weather_data(city_name)
        
        if weather_info:
            kelvin = 273
            temp = int(weather_info['main']['temp'] - kelvin)
            feels_like_temp = int(weather_info['main']['feels_like'] - kelvin)
            pressure = weather_info['main']['pressure']
            humidity = weather_info['main']['humidity']
            wind_speed = weather_info['wind']['speed'] * 3.6
            sunrise = weather_info['sys']['sunrise']
            sunset = weather_info['sys']['sunset']
            timezone = weather_info['timezone']
            cloudy = weather_info['clouds']['all']
            description = weather_info['weather'][0]['description']

            sunrise_time = time_format_for_location(sunrise + timezone)
            sunset_time = time_format_for_location(sunset + timezone)

            weather_data = {
                "city": city_name,
                "temperature": temp,
                "feels_like": feels_like_temp,
                "pressure": pressure,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "sunrise": sunrise_time,
                "sunset": sunset_time,
                "cloudy": cloudy,
                "description": description
            }

            extreme_conditions = check_extreme_weather(temp, wind_speed, humidity, description)
            if extreme_conditions:
                messages.warning(request, "Extreme Weather Conditions:\n" + "\n".join(extreme_conditions))
        else:
            messages.error(request, f"Weather for '{city_name}' not found! Kindly enter a valid city name.")

    return render(request, 'weather/weather.html', {"weather_data": weather_data})

def check_extreme_weather(temp, wind_speed, humidity, description):
    extreme_conditions = []

    if temp > 30:
        extreme_conditions.append(f"High Temperature: {temp}°C")
    if temp < 0:
        extreme_conditions.append(f"Low Temperature: {temp}°C")
    if wind_speed > 50:
        extreme_conditions.append(f"High Wind Speed: {wind_speed} km/h")
    if humidity > 90:
        extreme_conditions.append(f"High Humidity: {humidity}%")
    if "storm" in description.lower():
        extreme_conditions.append(f"Storm: {description}")

    return extreme_conditions

# Create your views here.
