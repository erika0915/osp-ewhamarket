from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import sys

application  = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"

DB = DBhandler()

@application.route("/")
def hello():
    return render_template("index.html")

@application.route("/login")
def login():
    return render_template("login.html")

@application.route("/signup")
def signup():
    return render_template("signup.html")

@application.route("/signup_post", methods=['POST'])
def register_user():
    data=request.form
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data,pw_hash):
        return render_template("login.html")
    else:
        flash("user id already exist!")
        return render_template("signup.html")

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)