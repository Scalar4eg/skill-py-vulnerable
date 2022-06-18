from flask import request

IP_LIST = {}
IP_MAX_FAILS = 10


# Вызывается когда кто-то присылает неверный логин и пароль
def failed_attempt():
    ip = request.remote_addr  # IP-адрес клиента делающего запрос
    if ip not in IP_LIST:
        IP_LIST[ip] = 0
    IP_LIST[ip] += 1


# Вызывается когда надо узнать забанен ли человек или нет
def is_banned():
    ip = request.remote_addr
    if ip not in IP_LIST:
        return False
    return IP_LIST[ip] > IP_MAX_FAILS
