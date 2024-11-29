from flask import Blueprint

# Blueprint 초기화
products_bp = Blueprint("products", __name__, template_folder="../../templates/products")

# routes.py 파일에서 라우트를 가져오기
from . import routes
