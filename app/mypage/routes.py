from flask import render_template, request, flash, redirect, url_for, session
from . import mypage_bp

# 마이페이지 조회 
@mypage_bp.route("/")
def view_mypage():
    # 세션에서 현재 로그인된 사용자 정보 가져오기 
    userId = session.get("userId")
    if not userId:
        flash("로그인 후에 마이페이지를 이용할 수 있습니다.")
        return redirect(url_for("auth.login"))
    
    # 사용자 정보 조회 
    userInfo = mypage_bp.db.get_user_info(userId)

    # 구매 목록 조회 
    purchasedList = mypage_bp.db.get_purchased_list(userId)

    # 판매 목록 조회 
    sellList = mypage_bp.db.get_sell_list(userId)

    return render_template("mypage.html",
                           nickname=userInfo.get("nickname"),
                           email=userInfo.get("email"),
                           profileImage = userInfo.get("profileImage"),
                           purchasedList=purchasedList,
                           sellList=sellList)