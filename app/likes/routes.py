from flask import jsonify, session, request
from . import likes_bp

# 좋아요 상태 조회
@likes_bp.route('/show_heart/<productId>/', methods=['GET'])
def show_heart(productId):
    userId = session.get('userId')
    if not userId:
        return jsonify({'error': '로그인이 필요합니다!'}), 401

    my_heart = likes_bp.db.get_heart_by_Id(userId, productId)
    return jsonify({'my_heart': my_heart})

# 좋아요 등록
@likes_bp.route('/like/<productId>/', methods=['POST'])
def like(productId):
    userId = session.get('userId')
    if not userId:
        return jsonify({'error': '로그인이 필요합니다!'}), 401

    likes_bp.db.update_heart(userId, productId, 'Y')
    return jsonify({'msg': '좋아요 완료!'})

# 좋아요 취소
@likes_bp.route('/unlike/<productId>/', methods=['POST'])
def unlike(productId):
    userId = session.get('userId')
    if not userId:
        return jsonify({'error': '로그인이 필요합니다!'}), 401

    likes_bp.db.update_heart(userId, productId, 'N')
    return jsonify({'msg': '좋아요 취소 완료!'})
