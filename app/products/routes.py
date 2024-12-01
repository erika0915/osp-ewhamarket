from flask import render_template, request, flash, redirect, url_for, session 
from . import products_bp
import math
from datetime import datetime,timezone


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
    data = products_bp.db.get_products()  # 데이터베이스 핸들러에서 데이터를 가져옵니다
    if not data:
        flash("DB에 데이터가 없습니다.")
        return render_template("products.html", total=0, datas=[], page_count=0, m=row_count)

    # 페이지네이션 처리 및 정렬
    start_idx = per_page * page
    end_idx = per_page * (page + 1)
    if category == "all":
        data = products_bp.db.get_products()
    else:
        data = products_bp.db.get_products_bycategory(category)
  
    # 버튼별 정렬 
    for key, value in data.items():
        if "created_at" not in value or not value["created_at"]:
            value["created_at"] = datetime.now(timezone.utc).isoformat() 
    def safe_datetime(value):
        try:
            return datetime.fromisoformat(value)
        except (ValueError, TypeError):
             datetime.min

    if sort_by=="all":
        # 기본 정렬
        data=dict(sorted(data.items(), key=lambda x: x[0]))
    elif sort_by == "recent":
        # 최신순
        data=dict(sorted(data.items(), key=lambda x: datetime.fromisoformat(x[1]["created_at"]), reverse=True))
    #data = dict(sorted(data.items(), key=lambda x: x[0]["created_at"], reverse=False))
    item_counts = len(data)

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

    # 템플릿 렌더링
    return render_template(
        "products.html",
        datas=paginated_data.items(),
        row1=row_data[0].items() if len(row_data) > 0 else [],
        row2=row_data[1].items() if len(row_data) > 1 else [],
        limit=per_page,
        page=page,
        page_count=int(math.ceil(item_counts / per_page)),
        total=item_counts,
        category=category,
        sort_by=sort_by,
        m=row_count
    )

# 상품 상세 조회
@products_bp.route("/<name>/")
def view_product_detail(name):
    data = products_bp.db.get_product_byname(str(name))
    return render_template("product_detail.html", name=name, data=data)

# 상품 등록
@products_bp.route("/reg_product", methods=["GET", "POST"])
def reg_product():
     # 로그인해야 상품 등록 할 수 있도록 
    userId = session.get('userId')
    #nickname = session.get("nickname")
    if not userId:
        flash("로그인 후에 상품 등록이 가능합니다!")
        return redirect(url_for("auth.login"))

    if request.method == "GET":
        return render_template("reg_product.html")

    elif request.method == "POST":
        image_file = request.files.get("productImage")
        image_file.save(f"static/images/{image_file.filename}")
        #to_dict로 수정해서 키값을 통해 data['price']처럼 쉽게 정보 가져올 수 있음 
        data = request.form.to_dict()
        #등록 시간 서버 자동 저장 
        current_time = datetime.utcnow().isoformat() 
        data['createdAt'] = current_time 
     
    if products_bp.db.insert_product(userId, data, image_file.filename):
        flash("상품이 성공적으로 등록되었습니다!")
        return redirect(url_for("products.view_products"))

@products_bp.route("/purchase_now",methods=["GET", "POST"])
def purchase_now():
    if request.method == "GET":
        flash("구매 완료")
        return render_template("product_detail.html")

    elif request.method == "POST":
        image_file = request.files.get("productImage")
        image_file.save(f"static/images/{image_file.filename}")
        #to_dict로 수정해서 키값을 통해 data['price']처럼 쉽게 정보 가져올 수 있음 
        data = request.form.to_dict()
        #구매시간 서버 자동 저장 
        #current_time = datetime.now().isoformat() 
        #data['purchaseAt'] = current_time 
        # -> db에 추가해야함... 
