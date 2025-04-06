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
       
            print(foxes)
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
                                text = f"Oшибка")

# Сработает если ошибка 404 - т.е. любой другой путь который выше не предусмотрен


@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red">такой страницы не существует</h1>'


app.run(debug=True)