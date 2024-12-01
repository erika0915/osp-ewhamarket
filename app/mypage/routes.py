from flask import render_template, request, flash, redirect, url_for
from . import mypage_bp

# 마이페이지 조회 
@mypage_bp.route("/")
def view_mypage():
    return render_template("mypage.html")