from flask import jsonify, session, request
from . import likes_bp

# 좋아요 상태 조회
@likes_bp.route('/show_heart/<productName>/', methods=['GET'])
def show_heart(productName):
    userId = session.get('userId')
    if not userId:
        return jsonify({'error': '로그인이 필요합니다!'}), 401

    my_heart = likes_bp.db.get_heart_byname(userId, productName)
    return jsonify({'my_heart': my_heart})

# 좋아요 등록
@likes_bp.route('/like/<productName>/', methods=['POST'])
def like(productName):
    userId = session.get('userId')
    if not userId:
        return jsonify({'error': '로그인이 필요합니다!'}), 401

    likes_bp.db.update_heart(userId, 'Y', productName)
    return jsonify({'msg': '좋아요 완료!'})

# 좋아요 취소
@likes_bp.route('/unlike/<productName>/', methods=['POST'])
def unlike(productName):
    userId = session.get('userId')
    if not userId:
        return jsonify({'error': '로그인이 필요합니다!'}), 401

    likes_bp.db.update_heart(userId, 'N', productName)
    return jsonify({'msg': '좋아요 취소 완료!'})
