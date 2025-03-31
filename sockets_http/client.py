"""

написать приложение-клиент используя модуль socket работающее в домашней 
локальной сети.
Приложение должно соединятся с сервером по известному адрес:порт и отправлять 
туда текстовые данные.

известно что сервер принимает данные следующего формата:
    "command:reg; login:<login>; password:<pass>" - для регистрации пользователя
    "command:signin; login:<login>; password:<pass>" - для входа пользователя
    
    
с помощью программы зарегистрировать несколько пользователей на сервере и произвести вход


"""
import socket

HOST = ('127.0.0.1', 7779)



# регистрация пользователя:
def user_register(login,password):

    global HOST
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(HOST)
    sock.sendall((f"command:reg; login:{login}; password:{password}").encode("utf-8"))
    data = sock.recv(1024).decode("utf-8")
    print(data)

    sock.close() 


# вход пользователя:
def user_signing(login,password):

    global HOST
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(HOST)
    sock.sendall((f"command:signin; login:{login}; password:{password}").encode("utf-8"))
    data = sock.recv(1024).decode("utf-8")
    print(data)

    sock.close() 

user_register('Vasja','yuy0990')
user_register('Dimas','HDerr23')
user_signing('Vasja','yuy0990')
user_signing('Dimas','HDerr23')



   