import time
import uuid
from os import environ
from secrets import token_urlsafe

from dotenv import load_dotenv

from flask import Flask, redirect, render_template, request

from ip_ban import failed_attempt, is_banned
from memory_session import start_session, load_session, session_exists, drop_session

app = Flask(__name__, static_url_path='/', static_folder='./')
app.config['SECRET_KEY'] = token_urlsafe(32)

WALL = {
    "text": ""
}

def run_app():
    load_dotenv()
    app.run(host=environ.get("APP_HOST"), port=environ.get("APP_PORT"))


def get_password():
    return environ.get("VULNERABLE_PASSWORD")


def get_login():
    return environ.get("VULNERABLE_LOGIN")


@app.route("/wall")
def wall_page():
    return render_template("drawing-wall.html", wall_text = WALL["text"])



@app.route("/")
def index():
    return redirect("/login")


@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/api/wall")
def wall_api():
    global WALL
    WALL["text"] = request.args["wall_text"]
    return {"result": True}

@app.route("/api/login-with-password", methods=['POST'])
def login_with_password():
    if is_banned():
        error = f"IP {request.remote_addr} Banned"
        print(error)
        return error, 500
    login = request.form["login"]
    password = request.form["password"]


    # Проверка логина и пароля
    if login == get_login() and password == get_password():
        # Если правильные
        sess = start_session()
        new_token = uuid.uuid4()  # Генерируем случайную строчку
        sess["token"] = new_token  # Запоминаем для этого пользователя

        return {"result": True, "redirect": "/secret-page"}
    else:
        failed_attempt()
        return {"result": False}


@app.route("/secret-page")
def secret_page():
    if session_exists():
        sess = load_session()
        return render_template("secret-page.html", my_secret=environ.get("MY_SECRET"), token = sess["token"])
    else:
        return redirect("/login")


@app.route("/logout")
def logout():
    token = request.args.get("token", "")
    sess = load_session()
    if token != sess["token"]:  # Сравниваем токены
        return {"result": False, "error": "Invalid Token"}

    drop_session()
    return redirect("/login")


if __name__ == '__main__':
    run_app()
