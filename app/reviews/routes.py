from flask import render_template, request, flash, redirect, url_for
from . import reviews_bp
import os 

# 리뷰 리스트
@reviews_bp.route("/")
def view_reviews():
    page = request.args.get("page", 0, type=int)
    per_page = 4
    per_row = 2
    row_count = int(per_page / per_row)

    # 데이터베이스에서 리뷰 가져오기
    data = reviews_bp.db.get_reviews()
    if not data:
        flash("DB에 데이터가 없습니다.")
        return render_template("reviews.html", total=0, datas=[], page_count=0, m=row_count)

    # 데이터 변환 및 페이지네이션
    all_reviews = [
        {
            "product": product,
            "review_id": review_id,
            "userId": review.get("userId"),
            "title": review.get("title"),
            "content": review.get("content"),
            "rate": review.get("rate"),
            "reviewImage": review.get("reviewImage"),
        }
        for product, reviews in data.items()
        for review_id, review in reviews.items()
    ]

    start_idx = page * per_page
    end_idx = start_idx + per_page
    paginated_reviews = all_reviews[start_idx:end_idx]

    # 행 단위 데이터 나누기
    rows = [paginated_reviews[i * per_row : (i + 1) * per_row] for i in range(row_count)]

    # 템플릿 렌더링
    return render_template(
        "reviews/reviews.html",
        total=len(all_reviews),
        datas=paginated_reviews,
        row1=rows[0] if len(rows) > 0 else [],
        row2=rows[1] if len(rows) > 1 else [],
        page=page,
        page_count=(len(all_reviews) + per_page - 1) // per_page,
        m=row_count,
    )

# 리뷰 상세 조회
@reviews_bp.route("/<productName>/<review_id>")
def view_review_detail(productName, review_id):
    review = reviews_bp.db.get_review_by_id(productName, review_id)
    return render_template("reviews/review_detail.html", review=review)

# 리뷰 등록
@reviews_bp.route("/reg_review/<productName>", methods=["GET", "POST"])
def reg_review(productName):
    if request.method == "GET":
        return render_template("reviews/reg_review.html", productName=productName)

    elif request.method == "POST":
        image_file = request.files.get("reviewImage")
        if not image_file:
            flash("이미지 파일을 업로드해주세요.")
            return redirect(url_for("reviews.reg_review", productName=productName))
        image_file.save(f"static/images/{image_file.filename}")

        data = request.form
        reviews_bp.db.insert_review(productName, data, image_file.filename)
        flash("리뷰가 성공적으로 등록되었습니다!")
        return redirect(url_for("reviews.view_reviews"))

# 상품 별 리뷰 상세 조회
@reviews_bp.route("/<productName>")
def view_product_reviews(productName):
    reviews, product_image = reviews_bp.db.get_review_by_name(productName)
    return render_template(
        "product_review_details.html",  # 템플릿 경로 수정
        productName=productName,
        reviews=reviews,
        productImage=product_image
    )