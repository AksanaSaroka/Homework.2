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

HOST = ('127.0.0.1', 7771)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(HOST)


sock.sendall('command:reg; login:<login>; password:<pass>'.encode("utf-8"))
data = sock.recv(1024).decode("utf-8")
# print(data) 





sock.close()    