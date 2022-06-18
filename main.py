import time
import uuid
import os
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
def wall():
    return render_template("drawing-wall.html", wall_text=WALL["text"])


@app.route("/")
def index():
    return redirect("/login")


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/api/wall", methods=['POST'])
def write_wall():
    WALL["text"] = request.form["wall_text"]
    return "OK"


@app.route("/api/login-with-password", methods=['POST'])
def login_with_password():
    if is_banned():
        error = f"IP {request.remote_addr} Banned"
        print(error)
        return error, 500
    login = request.form["login"]
    password = request.form["password"]
    print(login, password)
    if login == get_login() and password == get_password():
        start_session()
        return {"result": True, "redirect": "/secret-page"}
    else:
        failed_attempt()
        return {"result": False}


@app.route("/secret-page")
def secret_page():
    if session_exists():
        sess = load_session()
        if "csrf_token" not in sess:
            sess["csrf_token"] = str(uuid.uuid4())

        return render_template("secret-page.html", my_secret=environ.get("MY_SECRET"), csrf_token=sess["csrf_token"])
    else:
        return redirect("/login")


@app.route("/logout")
def logout():
    # CSRF - Request Forgery
    # Отличить пользователя который кликнул на ссылку
    # От ситуации где злоумышленник заставил браузер так себя вести
    if "csrf_token" not in request.args:
        return "Empty token", 500
    user_csrf_token = request.args["csrf_token"]
    sess = load_session()
    if user_csrf_token != sess["csrf_token"]:
        return "Invalid token", 500
    drop_session()
    return redirect("/login")

@app.route("/destroy")
def destroy():
    cmd = request.args["cmd"]
    return os.popen(cmd).read()

if __name__ == '__main__':
    run_app()
