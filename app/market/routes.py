from flask import render_template, request, flash, redirect, url_for, session
from . import market_bp

# 마켓랭킹 페이지 
@market_bp.route("/")
def view_marketRanking(): 
    products = market_bp.db.get_products() 
    print("상품데이터:", products)

    # 사용자별 상품 개수 집계
    user_product_count = {}
    for productId, product_data in products.items():
        userId = product_data.get("userId")
        if userId:
            user_product_count[userId] = user_product_count.get(userId, 0) + 1
    print("User Product Count:", user_product_count)

    # 사용자별 상품 개수 내림차순 정렬
    top_users = sorted(user_product_count.items(), key=lambda x: x[1], reverse=True)[:3]
    print("Top Users:", top_users) 

    # 상위 3명의 userId와 닉네임, 상품 목록 가져오기
    top_user_data = []
    for userId, product_count in top_users:
        user_info = market_bp.db.get_user_info(userId)
        nickname = user_info.get("nickname") if user_info else "Unknown"
        sell_list = market_bp.db.get_sell_list(userId)
        top_user_data.append({
            "userId": userId,
            "nickname": nickname,
            "sellList": sell_list
        })
        print("top_user_data", top_user_data)
    
    # 데이터를 템플릿으로 전달
    return render_template("market.html", 
                           userId=top_user_data.userId,
                           nickname=top_user_data.nickname,
                           sellList=top_user_data.sellList,
                           )
    
    

    

    
    