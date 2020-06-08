import requests
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weatherData.db'
database = SQLAlchemy(app)

class City(database.Model):
    id = database.Column(database.Interval, primary_key=True)
    name = database.Column(database.String(50), nullable=False)


@app.route('/')
def index():
    cities
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=8ad2342bc9de1e81734e896a48a13c93'
    city = 'Guangzhou'
    response = requests.get(url.format(city)).json()
    # print(response)

    weather_data = {
        'City': city,
        'Temperature': response['main']['temp'],
        'Description': response['weather'][0]['description'],
        'Icon': response['weather'][0]['icon'],
        'Temperature_Max': response['main']['temp_max'],
        'Temperature_Min': response['main']['temp_min'],
        'Humidity': response['main']['humidity'],
        'Pressure': response['main']['pressure'],
        'Wind': response['wind']['speed']
    }
    print(weather_data)
    return render_template('weather.html', weather_data=weather_data)
