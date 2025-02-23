import requests
from django.shortcuts import render
from django.conf import settings

def get_weather(request):
    pollution_data = {}
    
    if request.method == "POST":
        city = request.POST.get('city')
        api_key = "4756c9dbcb4e33cc8c9d6467219fd099"  # Replace with your OpenWeatherMap API key
        
        # Step 1: Get latitude and longitude from city name
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()

        if geo_data:
            lat = geo_data[0]['lat']
            lon = geo_data[0]['lon']

            # Step 2: Fetch air pollution data
            pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
            response = requests.get(pollution_url)
            data = response.json()

            if 'list' in data:
                pollution_info = data['list'][0]  # Get the first record
                pollution_data = {
                    'city': city,
                    'aqi': pollution_info['main']['aqi'],  # Air Quality Index (1-5)
                    'co': pollution_info['components']['co'],   # Carbon Monoxide
                    'no2': pollution_info['components']['no2'],  # Nitrogen Dioxide
                    'so2': pollution_info['components']['so2'],  # Sulfur Dioxide
                    'pm2_5': pollution_info['components']['pm2_5'],  # Particulate Matter 2.5
                    'pm10': pollution_info['components']['pm10'],  # Particulate Matter 10
                }
            else:
                pollution_data = {'error': 'Air pollution data not found.'}
        else:
            pollution_data = {'error': 'City not found. Please try again.'}
    
    return render(request, 'weather/index.html', {'pollution_data': pollution_data})
