from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import sys 

application  = Flask(__name__, static_folder='static')
application.config["SECRET_KEY"]="helloosp"
DB = DBhandler()

# 첫 화면 
@application.route("/")
def hello() :
    #return render_template("index.html")
    return redirect(url_for('view_list'))

# 상품 등록 조회 
@application.route('/reg_product')
def reg_items():
    return render_template('reg_product.html')

# 상품 등록 요청 
@application.route("/reg_product_post", methods=['POST'])
def reg_item_submit_post():

    image_file = request.files["file"]

    image_file.save("static/images/{}".format(image_file.filename))
    data = request.form 
    print(request.form)
    DB.insert_item(data['productName'], data, image_file.filename)
    return render_template("submit_item_result.html", data=data, img_path = "static/images/{}".format(image_file.filename))
    #reg_items

# 전체 상품 조회 
@application.route("/products")
def view_list(): 
    page = request.args.get("page", 0, type = int) 
    per_page = 6 
    per_row = 3 
    row_count = int(per_page/per_row)

    data = DB.get_items() 
    if not data:
        print("DB에 데이터가 없습니다.")
        return render_template("products.html", total=0, datas=[], page_count=0, m=row_count)

    start_idx = per_page * page
    end_idx = per_page * (page+1)
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)
    for i in range(row_count):
        if (i == row_count -1) and (tot_count % per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])
            
    print(f"item_counts: {item_counts}, page_count: {int((item_counts / per_page) + 1)}")
    print(f"data: {data}")
    return render_template(
        "products.html", 
        datas = data.items(),
        row1 = locals()['data_0'].items(), 
        row2 = locals()['data_1'].items(), 
        limit = per_page, 
        page = page, 
        page_count = int((item_counts / per_page) + 1), 
        total = item_counts, 
        m=row_count
    )

    print(f"item_counts: {item_counts}, per_page: {per_page}, page_count: {page_count}")


#@application.route('/dynamicurl/<variable_name>/')
# def DynamicUrl(variable_name):
#    return str(variable_name)

# 상품 상세 조회 
@application.route("/products/<name>/")
def view_item_detail(name):
    print("###name:", name)
    data = DB.get_item_byname(str(name))
    print("###data:", data)
    return render_template("product_detail.html", name=name, data=data)

# 로그인 조회 
@application.route("/login")
def login():
    return render_template("login.html")

# 로그인 요청 
@application.route("/login_confirm", methods=['POST'])
def login_user():
    id_=request.form['id']
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id_,pw_hash):
        session['id']=id_
        return redirect(url_for('view_list'))
    else:
        flash("Wrong ID or PW!")
        return render_template("login.html")

# 로그아웃 
@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('view_list'))

# 회원가입 조회 
@application.route("/signup")
def signup():
    return render_template("signup.html")

# 회원가입 요청 
@application.route("/signup_post", methods=['POST'])
def register_user():
    data=request.form
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data,pw_hash):
        return render_template("login.html")
    else:
        flash("user id already exist!")
        return render_template("signup.html")

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)


