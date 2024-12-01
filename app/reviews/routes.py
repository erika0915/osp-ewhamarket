from flask import render_template, request, flash, redirect, url_for
from . import reviews_bp
import os 
from datetime import datetime 

# 리뷰 리스트
@reviews_bp.route("/")
def view_reviews():
    page = request.args.get("page", 0, type=int)
    per_page = 4
    per_row = 2
    row_count = int(per_page / per_row)

    # 데이터베이스에서 리뷰 가져오기
    all_reviews = reviews_bp.db.get_reviews()
    if not all_reviews:
        flash("DB에 데이터가 없습니다.")
        return render_template("reviews.html", total=0, datas=[], page_count=0, m=row_count)

    # 데이터 변환
    review_list = [
        {
            "reviewId" : reviewId,
            "productId" : review.get("productId"),
            "userId" : review.get("userId"),
            "title" : review.get("title"),
            "content": review.get("content"),
            "rate" : review.get("reviewStar"),
            "reviewImage" : review.get("reviewImage")
        }
        for reviewId, review in all_reviews.items()
    ]

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
        m=row_count,
    )

# 리뷰 상세 조회
@reviews_bp.route("/<reviewId>")
def view_review_detail(reviewId):
    review = reviews_bp.db.get_review_by_id(reviewId)
    return render_template("review_detail.html", review=review)

# 리뷰 등록
@reviews_bp.route("/reg_review/<productName>", methods=["GET", "POST"])
def reg_review(productName):
    # 상품 이름이 전달된 값과 같은 데이터를 조회 
    product = reviews_bp.db.child("products").order_by_child("productName").equal_to(productName).get().val()
    
    # 조회된 결과의 상품 ID를 가져옴 
    productId = list(product.keys())[0]

    # 상품 ID를 사용해 해당 상품의 데이터를 조회 
    productData = product[productId]

    if request.method == "GET":
        return render_template("reg_review.html", 
                               productId = productId, 
                               productName=productData.get("productName"))

    elif request.method == "POST":
        image_file = request.files.get("reviewImage")
        if not image_file:
            flash("이미지 파일을 업로드해주세요.")
            return redirect(url_for("reviews.reg_review", productName=productName))
        image_file.save(f"static/images/{image_file.filename}")

        # 리뷰 데이터 구성 
        data = request.form
        data["productId"] = productId
        data["createdAt"] = datetime.utcnow().isoformat() 

        # 리뷰 저장 
        reviews_bp.db.insert_review(data, image_file.filename)
        flash("리뷰가 성공적으로 등록되었습니다!")
        return redirect(url_for("reviews.view_reviews"))

# 상품 별 리뷰 상세 조회
@reviews_bp.route("/<productName>")
def view_product_reviews(productName):
    # 상품 명을 통해서 상품 ID 조회 
    product = reviews_bp.db.child("products").order_by_child("productName").equal_to(productName).get().val()
    
    # 상품 ID 가져오기 
    productId = list(product.keys())[0]

    # 리뷰 조회 
    reviews, product_image = reviews_bp.db.get_review_by_product(productId)
    return render_template(
        "product_review_details.html",
        productName=productName,
        reviews=reviews,
        productImage=product_image
    )