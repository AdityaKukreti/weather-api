import requests
from flask import Flask, render_template, request
import os

app = Flask(__name__)

class WeatherData:
    name = None
    region = None
    country = None
    temp = {'celcius': None, 'fahrenheit': None}
    wind = {'mph': None, 'kph': None}
    humidity = None
    weather = None

    def __init__(self):
        pass

api_key = os.getenv('weather_api')
base_url = "http://api.weatherapi.com/v1"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        response = requests.get(f"{base_url}/current.json?key={api_key}&q={city}").json()

        if response.get('error'):
            if response['error']['code'] == 1006:
                error_message = "No matching location found."
            else:
                error_message = response['error']['message']
            return render_template('index.html', error=error_message)

        data = WeatherData()
        data.country = response['location']['country']
        data.name = response['location']['name']
        data.region = response['location']['region']
        data.humidity = response['current']['humidity']
        data.weather = response['current']['condition']['text']
        data.temp = {'celcius': response['current']['temp_c'], 'fahrenheit': response['current']['temp_f']}
        data.wind = {'mph': response['current']['wind_mph'], 'kph': response['current']['wind_kph']}

        return render_template('index.html', weather_data=data)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=10000)
