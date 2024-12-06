from flask import Blueprint

# Blueprint 초기화
market_bp = Blueprint("market", __name__, template_folder="../../templates")

# routes.py에서 라우트를 가져오기
from . import routes