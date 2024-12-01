from flask import Flask, redirect, url_for
from database import DBhandler  # DB 핸들러 가져오기

def create_app():
    app = Flask(__name__, static_folder="../static", template_folder="../templates")
    app.config["SECRET_KEY"] = "helloosp"

    # 데이터베이스 핸들러
    db = DBhandler()  # 전역 DB 핸들러 등록

    # Blueprint 가져오기
    from app.products import products_bp
    from app.reviews import reviews_bp
    from app.auth import auth_bp
    from app.likes import likes_bp 
    from app.mypage import mypage_bp
    
    # Blueprint에 DB 핸들러 전달
    products_bp.db = db
    reviews_bp.db = db
    auth_bp.db = db
    likes_bp.db = db 
    mypage_bp.db = db 

    # Blueprint 등록
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(reviews_bp, url_prefix="/reviews")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(likes_bp, url_prefix="/likes")
    app.register_blueprint(mypage_bp, url_prefix="/mypage")

    # 메인 라우트
    @app.route("/")
    def hello():
        return redirect(url_for("products.view_products"))

    return app
