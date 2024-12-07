from flask import jsonify, render_template, request, redirect, url_for, session, flash
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
        nickname = auth_bp.db.find_user(userId, pw_hash)
        if nickname:
        #if auth_bp.db.find_user(userId, pw_hash):
            session["userId"]=userId
            session["nickname"] = nickname
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
        profile_image = request.files.get("file")
        
        # 비밀번호 해싱 
        pw_hash = hashlib.sha256(pw.encode("utf-8")).hexdigest()

        # 프로필 이미지 저장 
        if profile_image:
            image_path = f"static/images/{profile_image.filename}"
            profile_image.save(image_path)
        else:
            image_path = "static/images/profiles/default.jpg"  
    
        # 사용자 데이터 추가  
        if auth_bp.db.insert_user(data, pw_hash, profile_image.filename):
            return redirect(url_for("auth.login"))
        else:
            return render_template("signup.html")

#Id 중복체크버튼
@auth_bp.route("/idcheck", methods=["GET"])
def id_check():
    user_id = request.args.get("userId")  # 쿼리 문자열에서 userId를 가져옵니다
    if not user_id:
        return jsonify({"success": False, "message": "아이디를 입력하세요."}), 400

    is_available = auth_bp.db.user_duplicate_check(user_id)  # 중복 여부 확인
    if is_available:
        return jsonify({"success": True, "message": f"'{user_id}'는 사용 가능한 ID입니다."}),200
    else:
        return jsonify({"success": False, "message": f"'{user_id}'는 이미 사용 중인 ID입니다."}), 409
    
#nickname 중복체크버튼
@auth_bp.route("/nickcheck", methods=["GET"])
def nick_chek():
    nickname = request.args.get("nickname")  # 쿼리 문자열에서 nickname을 가져옵니다
    if not nickname:
        return jsonify({"success": False, "message": "닉네임을 입력하세요."}), 400

    is_available = auth_bp.db.nickname_duplicate_check(nickname)  # 중복 여부 확인
    if is_available:
        return jsonify({"success": True, "message": f"'{nickname}'는 사용 가능한 닉네임입니다."}),200
    else:
        return jsonify({"success": False, "message": f"'{nickname}'는 이미 사용 중인 닉네임입니다."}), 409