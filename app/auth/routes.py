from flask import render_template, request, redirect, url_for, session, flash
from . import auth_bp
import hashlib

# 로그인
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET": 
        return render_template("login.html")
    
    if request.method == "POST": 
        userId = request.form["userId"]
        pw = request.form["pw"]
        pw_hash = hashlib.sha256(pw.encode("utf-8")).hexdigest()

        if auth_bp.db.find_user(userId, pw_hash):
            session["userId"] = userId
            flash("로그인 되었습니다")
            return redirect(url_for("products.view_products"))
        else:
            flash("잘못된 아이디 또는 패스워드입니다.")
            return render_template("login.html")

# 로그아웃
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("로그아웃 되었습니다.")
    return redirect(url_for("products.view_products"))

# 회원가입 
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET": 
        return render_template("signup.html")

    if request.method == "POST":    
        data = request.form
        pw = data.get("pw")
        
        # 비밀번호 해싱 
        pw_hash = hashlib.sha256(pw.encode("utf-8")).hexdigest()

        # 사용자 추가 
        if auth_bp.db.insert_user(data, pw_hash):
            flash("회원가입이 완료되었습니다.")
            return redirect(url_for("auth.login"))
        else:
            flash("이미 존재하는 userId 입니다.")
            return render_template("signup.html")