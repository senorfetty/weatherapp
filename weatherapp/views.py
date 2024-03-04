from django.shortcuts import render
import requests
import os
from dotenv import load_dotenv

load_dotenv()
# Create your views here.

def format_timezone(offset_seconds):
    hours = offset_seconds // 3600
    minutes = (offset_seconds % 3600) // 60
    return f"{hours:+03d}:{minutes:02d}"

def index(request):
    city_error= ''

    if request.method == 'POST':
        city= request.POST.get('city')

        api_key= os.getenv('myapikey')
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

        response= requests.get(url)

        if response.status_code == 200:
            data= response.json()
            temp_kelvin = data['main']['temp']
            country_code= data['sys']['country']
            timezone_offset=data['timezone']
            temp= temp_kelvin - 273.15
            desc= data['weather'][0]['description']
            formatted_timezone = format_timezone(timezone_offset)

            return render(request, 'index.html', {'city':city, 'country_code':country_code, 'timezone':formatted_timezone, 'temp':temp , 'desc':desc})

        elif response.status_code == 404:
            city_error= f'The city "{city}" was not found please enter a valid city name'
       
    return render(request, 'index.html', {'city_error':city_error})