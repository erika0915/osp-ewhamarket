from flask import render_template, request, flash, redirect, url_for, session
from . import market_bp

# 마켓랭킹 페이지 
@market_bp.route("/")
def view_marketRanking(): 
    products = market_bp.db.get_products() 
    # 사용자별 등록 상품의 구매 수 집계
    user_purchase_count = {}
    for productId, product_data in products.items():
        userId = product_data.get("userId")
        purchase_count = product_data.get("purchaseCount", 0)
        if userId:
            user_purchase_count[userId] = user_purchase_count.get(userId, 0) + purchase_count
        print(userId, ":" , user_purchase_count[userId])

    # 마켓별 등록 상품 개수 상위 3명 
    top_users = sorted(user_purchase_count.items(), key=lambda x: x[1], reverse=True)[:3]
    print("Top Users:", top_users) 
    
    # 상위 3명의 닉네임, 상품 목록, 상품 이미지 가져오기
    top_user_data = []
    for userId, product_count in top_users:
        user_info = market_bp.db.get_user_info(userId)
        nickname = user_info.get("nickname") if user_info else "Unknown"
        sell_list = market_bp.db.get_sell_list(userId)


        top_user_data.append({"nickname": nickname, "sellList": sell_list})
        #print("top_user_data", top_user_data)
    
    # 데이터를 템플릿으로 전달
    return render_template("market.html", top_user_data=top_user_data, top_users=top_users, nickname=nickname, sellList=sell_list)
    
    
    

    
    