import csv
import requests
import os

OPENWEATHER_API_KEY = 'your_api_key'
OPENWEATHER_GEOCODING_URL = 'http://api.openweathermap.org/geo/1.0/direct'
OPENWEATHER_ONECALL_URL = 'https://api.openweathermap.org/data/3.0/onecall'

def create_city_csv():
    with open('data/city.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['City'])
        writer.writerows([
            ['New York'],
            ['Los Angeles'],
            ['Chicago'],
            ['Houston'],
            ['Phoenix']
        ])

def get_city_coordinates(city):
    params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY
    }
    response = requests.get(OPENWEATHER_GEOCODING_URL, params=params)
    data = response.json()
    return data[0]['lat'], data[0]['lon']

def get_weather_data(lat, lon):
    params = {
        'lat': lat,
        'lon': lon,
        'appid': OPENWEATHER_API_KEY
    }
    response = requests.get(OPENWEATHER_ONECALL_URL, params=params)
    return response.json()

def collect_weather_stats():
    with open('data/city.csv', mode='r') as file:
        reader = csv.DictReader(file)
        weather_stats = []
        for row in reader:
            lat, lon = get_city_coordinates(row['City'])
            weather_data = get_weather_data(lat, lon)
            weather_stats.append({
                'City': row['City'],
                'Temperature': weather_data['current']['temp'],
                'Humidity': weather_data['current']['humidity']
            })
        return weather_stats

def save_weather_stats(weather_stats):
    with open('data/city_stats.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['City', 'Temperature', 'Humidity'])
        writer.writeheader()
        for stat in weather_stats:
            writer.writerow(stat)

def get_top_n_cities(weather_stats, key, n=3):
    return sorted(weather_stats, key=lambda x: x[key])[:n]

if __name__ == "__main__":
    os.makedirs('data', exist_ok=True)
    create_city_csv()
    weather_stats = collect_weather_stats()
    save_weather_stats(weather_stats)
    top_coldest_cities = get_top_n_cities(weather_stats, 'Temperature')
    top_humid_cities = get_top_n_cities(weather_stats, 'Humidity', n=3)
    print("Top coldest cities:", top_coldest_cities)
    print("Top humid cities:", top_humid_cities)
