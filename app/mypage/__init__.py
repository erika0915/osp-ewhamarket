from flask import Blueprint

# Blueprint 초기화
mypage_bp = Blueprint("mypage", __name__)

# routes.py 파일에서 라우트를 가져오기
from . import routes
