'''
Добавить к прошлому проекту 2 страницы 
    - страницу с формой регистрации.
        Регистрация должна содержать имя фамилию возраст email логин пароль.
        После отправки формы регистрации проверить данные на валидность
            - имя фамилия - только русские буквы
            - логин - латинские цифры и _. От 6 до 20 символов
            - пароль - обязательно хотя бы 1 латинская маленькая, 1 заглавная и  1 цифр. От 8 до 15 символов.
            - * email - должен быть валидным
            - * возраст - целое число от 12 до 100
        При успешной проверке  добавить пользователя в базу/файл/список/словарь 
            и направить пользователя на форму входа.
        При выявлении ошибок снова показать форму, но уже с заполненными полями 
            и в любом месте формы показать список ошибок.
        
    - страницу с формой входа на сайт.
        - при успешном входе                             
            - пометить в сессиях что он залогинился
            - перенаправить на главную страницу
        - при ошибке показать форму снова, с сообщением об ошибке



Все прежние страницы сделать открытыми только для пользователей которые произвели вход на сайт.
Если пользователь не залогинился и переходит на них - перенаправлять его на форму входа. 
На фоме входа сделать ссылку на форму регистрации.

Если пользовался залогинился - на каждой странице сверху писать - "Приветствуем вас имя фамилия"

На главной странице показывать ссылку ВХОД и РЕГИСТРАЦИЯ для пользователей которые не вошли на сайт
и ссылку ВЫХОД для  пользователей которые вошли на сайт

Таким образом новый пользователь имеет доступ  только на главную страницу где есть ссылка на вход регистрацию.
После регистрации и входа он имеет доступ на все доступные страницы.

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

@app.route("/registration/")
def registration():
    return render_template('registration.html')

@app.route("/enter/")
def enter():
    return render_template('enter.html')


# Сработает если ошибка 404 - т.е. любой другой путь который выше не предусмотрен
@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red">такой страницы не существует</h1>'




app.run(debug=True)