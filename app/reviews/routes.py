from flask import render_template, request, flash, redirect, url_for, session 
from . import reviews_bp
import os 
from datetime import datetime 

# 리뷰 등록
@reviews_bp.route("/reg_review/<productId>", methods=["GET", "POST"])
def reg_review(productId):

    # 로그인 여부 확인 
    userId = session.get("userId")
    if not userId:
        flash("로그인 후에 리뷰 등록이 가능합니다!")
        return redirect(url_for("auth.login"))

    existing_reviews = reviews_bp.db.get_review_by_product(productId)
    for review in existing_reviews:
        if review["userId"] == userId:
            return redirect(url_for("reviews.view_review_detail", reviewId=review["reviewId"]))

    # 상품 데이터 가져오기 
    products = reviews_bp.db.child("products").get().val()

    # 사용자별로 productId 탐색 
    for userProducts in products.values():
        if productId in userProducts:
            productData = userProducts[productId]
            break

    productName = productData.get("productName")

    if request.method == "GET":
        return render_template("reg_review.html", 
                               productId = productId, 
                               productName=productName)

    elif request.method == "POST":
        image_file = request.files.get("reviewImage")
        image_file.save(f"static/images/{image_file.filename}")

        # 사용자 정보 가져오기 
        user  = reviews_bp.db.child("users").child(userId).get().val()
        nickname = user.get("nickname")

        data = request.form.to_dict()
        rate = data.get("rate")
        data["productId"] = productId
        data["userId"] = userId  
        data["nickname"]=nickname
        data["createdAt"] = datetime.utcnow().isoformat() 
        data["rate"]= int(rate)

        # 리뷰 저장 및 reviewId 생성
        reviewId = reviews_bp.db.insert_review(data, image_file.filename)

        # purchasedProducts에 reviewId 저장
        reviews_bp.db.update_purchased_product_review(userId, productId, reviewId)

        # 리뷰 카운트 업데이트
        review_count = productData.get("reviewCount", 0) + 1
        productData["reviewCount"] = review_count
        reviews_bp.db.update_product(productId, productData)

        flash("리뷰가 성공적으로 등록되었습니다!")
        return redirect(url_for("reviews.view_reviews", productId=productId,reviewId=reviewId))
   
# 전체 리뷰 조회 
@reviews_bp.route("/")
def view_reviews():
    page = request.args.get("page", 0, type=int)
    per_page = 4
    per_row = 2
    row_count = int(per_page / per_row)

    # 데이터베이스에서 리뷰 가져오기
    all_reviews = reviews_bp.db.get_reviews()
    if not all_reviews:
        return render_template("reviews.html", total=0, datas=[], page_count=0, m=row_count)

    # 데이터 변환
    review_list=[]
    for reviewId, review in all_reviews.items():
        product = reviews_bp.db.get_product_by_id(review.get("productId"))
        if product is None:
            productName = "unknown product"
        else:
            productName = product.get("productName")
            
        review_list.append({
            "reviewId": reviewId,
            "productId": review.get("productId"),
            "userId": review.get("userId"),
            "title": review.get("title"),
            "content": review.get("content"),
            "rate": review.get("rate"),
            "reviewImage": review.get("reviewImage"),
            "productName": productName
        })


    # 페이지네이션 
    start_idx = page * per_page
    end_idx = start_idx + per_page
    paginated_reviews = review_list[start_idx:end_idx]

    # 행 단위 데이터 나누기
    rows = [paginated_reviews[i * per_row : (i + 1) * per_row] for i in range(row_count)]

    # 템플릿 렌더링
    return render_template(
        "reviews.html",
        total=len(review_list),
        datas=paginated_reviews,
        row1=rows[0] if len(rows) > 0 else [],
        row2=rows[1] if len(rows) > 1 else [],
        page=page,
        page_count=(len(all_reviews) + per_page - 1) // per_page,
        m=row_count
    )

# 리뷰 상세 조회 
@reviews_bp.route("/<reviewId>")
def view_review_detail(reviewId):
    review = reviews_bp.db.get_review_by_id(reviewId)
    product = reviews_bp.db.get_product_by_id(review.get("productId"))
    return render_template("review_detail.html", 
                           review=review, 
                           product=product)
