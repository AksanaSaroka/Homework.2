'''
Написать веб-приложение на Flask со следующими ендпоинтами:
    - главная страница - содержит ссылки на все остальные страницы
    - /duck/ - отображает заголовок "рандомная утка №ххх" и картинка утки 
                которую получает по API https://random-d.uk/
                
    - /fox/<int>/ - аналогично утке только с лисой (- https://randomfox.ca), 
                    но количество разных картинок определено int. 
                    если int больше 10 или меньше 1 - вывести сообщение 
                    что можно только от 1 до 10
    
    - /weather-minsk/ - показывает погоду в минске в красивом формате
    
    - /weather/<city>/ - показывает погоду в городе указанного в city
    
    - по желанию добавить еще один ендпоинт на любую тему 
    
    
Добавить обработчик ошибки 404. (есть в example)
    

'''

from flask import Flask, render_template
import os
import requests
import random
from pyowm import OWM
from pprint import pprint

BASE_DIR = os.path.dirname(__file__)

app = Flask(__file__,
            static_folder=os.path.join(BASE_DIR, 'static'),
            template_folder=os.path.join(BASE_DIR, 'templates'))



@app.route("/")
def index():
    return render_template('index.html')

@app.route("/duck/")
def duck():
    response = requests.get('https://random-d.uk/api/v2/random')
    data = response.json()
    # print(data)
    # print(data['url'].split('/')[-1])
    return render_template('duck.html',
                           duck_photo_url = data['url'],
                           duck_photo_number = data['url'].split('/')[-1].split('.')[0] 
                           )

    
@app.route("/fox/")
@app.route("/fox/<int:count>/")
def fox(count=1):
    try:    
        foxes = []
        if 1<= count <= 10:
            while len(foxes) != count:
                response = requests.get('https://randomfox.ca/floof')
                foxes.append(response.json()['image'])

            # print(foxes)
            return render_template ('fox.html',
                                foxes = foxes,
                                count_fox = count,
                               )
        else:
            return render_template ('fox.html',
                                    text = "Возможное количество лисичек от 1 до 10"
                                    )

    except Exception as e:
        return render_template ('fox.html',
                                text = "Oшибка")
    

@app.route("/weather/")
@app.route("/weather/<string:city>/")
def weather_city(city='Minsk'):
    try:
        owm = OWM('87b7c330daf2579649274a648d33f753')
        manager = owm.weather_manager()
        obs = manager.weather_at_place(city)
        weather = obs.weather
        # pprint(obs.to_dict())
        weather_data = {
            'city' : city,
            'status': weather.status,
            'humidity': weather.humidity,
            'temp': weather.temp['temp'],
            'feels_like': weather.temp['feels_like'],
        }

        return render_template('weather_city.html',
                           city=city,
                           weather = weather_data,
                           temp = round((weather.temp['temp'] - 273.5),1),
                           feels_like = round((weather.temp['feels_like'] - 273.5),1)
                           )
    
    except Exception as e:
        return render_template ('weather_city.html',
                                text = "Oшибка")
    
@app.route("/weather/Minsk/")
def weather_minsk():
    return weather_city(city='Minsk')


# Сработает если ошибка 404 - т.е. любой другой путь который выше не предусмотрен
@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red">такой страницы не существует</h1>'


app.run(debug=True)