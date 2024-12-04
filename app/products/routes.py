from flask import render_template, request, flash, redirect, url_for, session 
from . import products_bp
import math
from datetime import datetime,timezone

# 상품 등록
@products_bp.route("/reg_product", methods=["GET", "POST"])
def reg_product():
    # 로그인 여부 확인 
    userId = session.get('userId')
    if not userId:
        flash("로그인 후에 상품 등록이 가능합니다!")
        return redirect(url_for("auth.login"))

    if request.method == "GET":
        return render_template("reg_product.html")

    elif request.method == "POST":
        image_file = request.files.get("productImage")
        image_file.save(f"static/images/{image_file.filename}")
        data = request.form.to_dict()
        current_time = datetime.utcnow().isoformat() 
        data['createdAt'] = current_time 
     
    if products_bp.db.insert_product(userId, data, image_file.filename):
        flash("상품이 성공적으로 등록되었습니다!")
        return redirect(url_for("products.view_products"))
    
# 전체 상품 조회
@products_bp.route("/")
def view_products():
    page = request.args.get("page", 0, type=int)
    category = request.args.get("category", "all")
    sort_by = request.args.get("sort", "all")
    per_page = 6
    per_row = 3
    row_count = int(per_page / per_row)

    # 데이터베이스에서 상품 가져오기
    data = products_bp.db.get_products() 
    item_counts = len(data)

    # 페이지네이션 처리 및 정렬
    start_idx = per_page * page
    end_idx = per_page * (page + 1)
    if category == "all":
        data = products_bp.db.get_products()
    else:
        data = products_bp.db.get_products_by_category(category)

    # 버튼별 정렬 
    for key, value in data.items():
        # 두 필드를 모두 확인
        if "createdAt" not in value and "created_at" not in value:
            value["createdAt"] = datetime.now(timezone.utc).isoformat()
        elif "created_at" in value:
            # created_at 값을 createdAt으로 변환
            value["createdAt"] = value.pop("created_at")
    for key, value in data.items():
        print(f"Before Sorting - Product ID: {key}, Created At: {value['createdAt']}")

    def safe_datetime(value):
        try:
            return datetime.fromisoformat(value)
        except (ValueError, TypeError,AttributeError):
             datetime.min

    if sort_by == "recent":
        data=dict(sorted(data.items(), key=lambda x: safe_datetime(x[1].get("createdAt","")), reverse=True))
    elif sort_by == "purchase":
        data = dict(sorted(data.items(), key=lambda x: int(x[1].get("purchaseCount", 0)), reverse=True))
    else:
        data=dict(sorted(data.items(), key=lambda x: x[1].get("productName",""),reverse=False))
    for key, value in data.items():
        print(f"Sorted - Product ID: {key}, Created At: {value['createdAt']}, Product Name: {value.get('productName')}")

    # 현재 페이지 데이터
    if item_counts <= per_page:
        paginated_data = dict(list(data.items())[:item_counts])
    else:
        paginated_data = dict(list(data.items())[start_idx:end_idx])

    # 행 데이터 분리
    tot_count = len(paginated_data)
    row_data = []
    for i in range(row_count):
        if (i == row_count - 1) and (tot_count % per_row != 0):
            row_data.append(dict(list(paginated_data.items())[i * per_row:]))
        else:
            row_data.append(dict(list(paginated_data.items())[i * per_row:(i + 1) * per_row]))
    
    # 카테고리 이름 변경 
    category_names = {
    "all": "전체 상품 조회",
    "fashion": "패션 악세서리",
    "digital": "디지털 악세서리",
    "tableware": "테이블웨어",
    "stationary": "스테이셔너리"
    }
    current_category_name = category_names.get(category)
    
    # 템플릿 렌더링
    return render_template(
        "products.html",
        datas=list(paginated_data.items()),
        row1=row_data[0].items() if len(row_data) > 0 else [],
        row2=row_data[1].items() if len(row_data) > 1 else [],
        limit=per_page,
        page=page,
        page_count=int(math.ceil(item_counts / per_page)),
        total=item_counts,
        sort_by=sort_by,
        category=category,
        m=row_count,
        current_category_name=current_category_name  
    )

# 상품 상세 조회
@products_bp.route("/<productId>/")
def view_product_detail(productId):
    data = products_bp.db.get_product_by_id(productId)
    if not data:
        flash("상품 정보를 찾을 수 없습니다.")
        return redirect(url_for("products.view_products"))
    return render_template("product_detail.html", productId=productId, data=data)


# 상품 구매 
@products_bp.route("/<productId>/purchase_now",methods=["POST"])
def purchase_now(productId):
        
    # 로그인 여부 확인 
    user_id = session.get("userId") 
    if not user_id:
        flash("로그인 후에 상품을 구매할 수 있습니다!")
        return redirect(url_for("auth.login"))
        
    # 데이터베이스에서 해당 상품의 purchaseCount 가져오기
    data=request.form.to_dict()
    image_file=request.files.get("productImage")
    product_name = data['productName']
    product = products_bp.db.get_product_by_productName(product_name)
    if not product:
        flash("상품을 찾을 수 없습니다.")
        return redirect(url_for("products.view_products"))

    # purchaseCount 업데이트
    current_count = product.get("purchaseCount", 0)
    updated_count = current_count + 1

    # 데이터베이스에 업데이트된 값 저장
    product["purchaseCount"] = updated_count
    products_bp.db.update_product(productId, product)

    # 상품 정보를 사용자의 purchasedProducts에 추가
    result = products_bp.db.add_purchased_product(user_id, data)
    if result:
        flash("구매가 완료되었습니다! 구매 내역에 추가되었습니다.")
    else:
        flash("구매 처리 중 오류가 발생했습니다.")

    return redirect(url_for("products.view_products"))
