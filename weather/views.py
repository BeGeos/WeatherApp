from django.shortcuts import render
import requests
import datetime

# Create your views here.


def send_api_request(city, request):
    url = 'https://api.openweathermap.org/data/2.5/weather?'
    api_key = ''
    payload = {'q': city, 'units': 'metric', 'appid': api_key, 'exclude': 'minutely'}
    send = requests.get(url, params=payload)
    if send.status_code != 200:
        # print(send.status_code)
        return {'message': 'City not Found'}
    response = send.json()
    # print(response)
    feels_like = round(response['main']['feels_like'])
    pressure = response['main']['pressure']
    humidity = response['main']['humidity']
    visibility = response['visibility']
    wind_speed = response['wind']['speed']
    try:
        rain = response['rain']['1h']
    except:
        rain = ''
    country = response['sys']['country']
    today = datetime.datetime.now().strftime("%H:%M, %d/%m")
    weather_description = response['weather'][0]
    description = weather_description['main']
    icon = weather_description['icon']
    weather_main = response['main']
    temp = round(weather_main['temp'])
    min_temp = round(weather_main['temp_min'])
    max_temp = round(weather_main['temp_max'])

    output_ctx = {'description': description, 'icon': icon, 'city': city,
                  'temp': temp, 'min_temp': min_temp, 'max_temp': max_temp,
                  'country': country.upper(), 'feels_like': feels_like, 'pressure': pressure,
                  'humidity': humidity, 'visibility': visibility/1000, 'wind_speed': wind_speed,
                  'today': today, 'rain': rain}

    return output_ctx


def main_display(request):
    return render(request, 'base-home.html')


def weather_forecast(request):
    if len(request.GET) == 0:
        return render(request, 'forecast-home.html')
    else:
        city = request.GET['city']
        context = send_api_request(city, request)

    return render(request, '2-day-forecast.html', context)


def bio(request):
    return render(request, 'bio.html')


def api(request):
    return render(request, 'api.html')
