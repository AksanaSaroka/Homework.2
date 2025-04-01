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

BASE_DIR = os.path.dirname(__name__)

app = Flask(__name__,
            static_folder=os.path.join(BASE_DIR, 'static'),
            template_folder=os.path.join(BASE_DIR, 'templates'))

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/duck/")
def sheet1():
    return render_template("1.html", h="HELLO 123456")

@app.route("/fox/<int:num>/")
def test(num):
    return f"тест номер {num} запущен"

# Сработает если ошибка 404 - т.е. любой другой путь который выше не предусмотрен
@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red">такой страницы не существует</h1>'


app.run(debug=True)