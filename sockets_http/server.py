'''
написать приложение-сервер используя модуль socket работающее в домашней 
локальной сети.
Приложение должно принимать данные с любого устройства в сети отправленные 
или через программу клиент или через браузер
    - если данные пришли по протоколу http создать возможность след.логики:
        - если путь "/" - вывести главную страницу
        
        - если путь содержит /test/<int>/ вывести сообщение - тест с номером int запущен
        
        - если путь содержит message/<login>/<text>/ вывести в консоль/браузер сообщение
            "{дата время} - сообщение от пользователя {login} - {text}"
        
        - если путь содержит указание на файл вывести в браузер этот файл
        
        - во всех остальных случаях вывести сообщение:
            "пришли неизвестные  данные по HTTP - путь такой то"
                   
         
    - если данные пришли НЕ по протоколу http создать возможность след.логики:
        - если пришла строка формата "command:reg; login:<login>; password:<pass>"
            - выполнить проверку:
                login - только латинские символы и цифры, минимум 6 символов
                password - минимум 8 символов, должны быть хоть 1 цифра
            - при успешной проверке:
                1. вывести сообщение на стороне клиента: 
                    "{дата время} - пользователь {login} зарегистрирован"
                2. добавить данные пользователя в список/словарь на сервере
            - если проверка не прошла вывести сообщение на стороне клиента:
                "{дата время} - ошибка регистрации {login} - неверный пароль/логин"
                
        - если пришла строка формата "command:signin; login:<login>; password:<pass>"
            выполнить проверку зарегистрирован ли такой пользователь на сервере:                
            
            при успешной проверке:
                1. вывести сообщение на стороне клиента: 
                    "{дата время} - пользователь {login} произведен вход"
                
            если проверка не прошла вывести сообщение на стороне клиента:
                "{дата время} - ошибка входа {login} - неверный пароль/логин"
        
        - во всех остальных случаях вывести сообщение на стороне клиента:
            "пришли неизвестные  данные - <присланные данные>"       
                 

'''

import socket
import re
from datetime import datetime
# import os

# file_dir = os.path.dirname(__file__)


HOST = ('127.0.0.1', 7779)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(HOST)
sock.listen(5)
users = {}
path = ''

OK = b'HTTP/1.1 200 OK\n'
HEADERS = b"Host: some.ru\nHost1: some1.ru\n\n"
ERR_404 = b'HTTP/1.1 404 Not Found\n\n'



def send_file(file_name, conn):
    try:
        with open(file_name.lstrip('/'), 'rb') as f:                   
            conn.send(OK)
            conn.send(HEADERS)
            conn.send(f.read())
            
    except IOError:
        print('нет файла')
        conn.send(ERR_404)
        
        
def is_file(path):        
    if path[-4:] in ['.jpg','.png','.gif', '.ico', '.txt'] or \
       path[-5:] in ['.html', '.json']:
            return True
    return False





def http_request(data):
        
        if path == '/':
            send_file('index.html', conn) 

        if is_file(path):
            send_file(path, conn)

        if path.startswith("/test/"):
            num = int(path.strip('/').split('/')[1])
            conn.send(OK)
            conn.send(HEADERS)  
            conn.send(f"тест с номером {num} запущен".encode())         
        else:
            conn.send(ERR_404)

def check_login(login):
        pattern_login =  r'^[a-zA-Z0-9-_]{6,}$'
        if re.search(pattern_login, login): 
            return True 


def check_password(password):
        pattern_pass = r'^(?=.*\d)[0-9a-zA-Z]{8,}$'
        if re.search(pattern_pass, password): 
            return True

def is_registered(login,users):
    return login in users

def no_http_request(data):
    if "reg" in data:
        if check_login(login) and check_password(password):
            users[login] = password
            conn.send(f"{datetime.now():%d.%m.%Y %H-%M} - пользователь {login} зарегистрирован".encode())
        else:
            conn.send(f"{datetime.now():%d.%m.%Y %H-%M} - ошибка регистрации {login} - неверный пароль/логин".encode())    
        

    if "signin" in data:
        if  is_registered(login,users):
            conn.send(f"{datetime.now():%d.%m.%Y %H-%M} - пользователем {login} произведен вход".encode())
        else:
           conn.send(f"{datetime.now():%d.%m.%Y %H-%M} - ошибка входа {login} - неверный пароль/логин".encode())


while True:

    print("---listen----")
    conn, addr = sock.accept()
    data = conn.recv(1024).decode()
    print(data)

    
    try:
        if data.startswith("GET") or data.startswith("POST"):
            method, path, ver  = data.split('\n')[0].split(" ", 2)        
            http_request(data)

        if data.startswith("command"):
            login = data.split(";", 2)[1].strip(" ").split(":")[1]      #"command:signin; login:<login>; password:<pass>"
            password = data.split(";", 2)[2].strip(" ").split(":")[1]
            no_http_request(data)
        
        else: 
             
            conn.send(f"Пришли неизвестные данные - {data}".encode())

    except Exception as e:
         print(f"Error: {e}")
        
    conn.close()
    print(users)