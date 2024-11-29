from flask import render_template, request, redirect, url_for, session, flash
from . import auth_bp
import hashlib

# 로그인 페이지
@auth_bp.route("/login")
def login():
    return render_template("login.html")

# 로그인 요청 처리
@auth_bp.route("/login_confirm", methods=["POST"])
def login_user():
    id_ = request.form["userId"]
    pw = request.form["pw"]
    pw_hash = hashlib.sha256(pw.encode("utf-8")).hexdigest()
    if auth_bp.db.find_user(id_, pw_hash):
        session["id"] = id_
        flash("로그인 되었습니다")
        return redirect(url_for("products.view_products"))
    else:
        flash("Wrong ID or PW!")
        return render_template("login.html")

# 로그아웃
@auth_bp.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for("products.view_products"))

# 회원가입 페이지
@auth_bp.route("/signup")
def signup():
    return render_template("signup.html")

# 회원가입 요청 처리
@auth_bp.route("/signup_post", methods=["POST"])
def register_user():
    data = request.form
    pw = request.form["pw"]
    pw_hash = hashlib.sha256(pw.encode("utf-8")).hexdigest()
    if auth_bp.db.insert_user(data, pw_hash):
        return render_template("login.html")
    else:
        flash("User ID already exists!")
        return render_template("signup.html")
