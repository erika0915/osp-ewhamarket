from flask import Blueprint

# Blueprint 초기화
auth_bp = Blueprint("auth", __name__,template_folder="../../templates/auth")

# routes.py 파일에서 라우트를 가져오기
from . import routes
