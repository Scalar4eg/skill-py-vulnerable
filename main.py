import uuid
from os import environ
from secrets import token_urlsafe

from dotenv import load_dotenv

from flask import Flask, redirect, render_template, request

from memory_session import start_session, load_session, session_exists, drop_session

app = Flask(__name__, static_url_path='/', static_folder='./')
app.config['SECRET_KEY'] = token_urlsafe(32)


def run_app():
    load_dotenv()
    app.run()


def get_password():
    return environ.get("VULNERABLE_PASSWORD")


def get_login():
    return environ.get("VULNERABLE_LOGIN")


@app.route("/")
def index():
    return redirect("/login")


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/api/login-with-password", methods=['POST'])
def login_with_password():
    login = request.form["login"]
    password = request.form["password"]
    print(login, password)
    if login == get_login() and password == get_password():
        start_session()
        return {"result": True, "redirect": "/admin-panel"}
    else:
        return {"result": False}


@app.route("/admin-panel")
def admin_panel():
    if session_exists():
        return render_template("admin-panel.html", my_secret=environ.get("MY_SECRET"))
    else:
        return redirect("/login")


@app.route("/logout")
def logout():
    drop_session()
    return redirect("/login")


if __name__ == '__main__':
    run_app()
