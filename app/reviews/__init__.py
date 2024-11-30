from flask import Blueprint

# Blueprint 초기화
reviews_bp = Blueprint("reviews", __name__, template_folder="../../templates/reviews")

# routes.py 파일에서 라우트를 가져오기
from . import routes
