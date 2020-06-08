import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weatherData.db'
database = SQLAlchemy(app)

class City(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(50), nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_city = request.form.get('city')
        print(new_city)
        if new_city:
            new_city_obj = City(name=new_city)
            database.session.add(new_city_obj)
            database.session.commit()

    cities = City.query.all()
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=8ad2342bc9de1e81734e896a48a13c93'

    weather_data_cities = []
    for city in cities:
        response = requests.get(url.format(city.name)).json()
        # print(response)
        weather_data = {
            'City': city.name,
            'Temperature': response['main']['temp'],
            'Description': response['weather'][0]['description'],
            'Icon': response['weather'][0]['icon'],
            'Temperature_Max': response['main']['temp_max'],
            'Temperature_Min': response['main']['temp_min'],
            'Humidity': response['main']['humidity'],
            'Pressure': response['main']['pressure'],
            'Wind': response['wind']['speed']
        }
        weather_data_cities.append(weather_data)
        weather_data_cities_first_half = weather_data_cities[len(weather_data_cities)//2:]
        weather_data_cities_second_half = weather_data_cities[:len(weather_data_cities)//2]

    return render_template('weather.html', weather_data_cities_first_half=weather_data_cities_first_half,
                           weather_data_cities_second_half=weather_data_cities_second_half)
