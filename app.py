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
@application.route('/reg_items')
def reg_items():
    return render_template('reg_items.html')

# 상품 등록 요청 
@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():

    image_file = request.files["file"]

    image_file.save("static/images/{}".format(image_file.filename))
    data = request.form 
    print(request.form)
    DB.insert_item(data['productName'], data, image_file.filename)
    return render_template("submit_item_result.html", data=data, img_path = "static/images/{}".format(image_file.filename))
    #reg_items

# 전체 상품 조회 
@application.route("/list")
def view_list(): 
    page = request.args.get("page", 0, type = int) 
    per_page = 6 
    per_row = 3 
    row_count = int(per_page/per_row)

    data = DB.get_items() 
    if not data:
        print("DB에 데이터가 없습니다.")
        return render_template("list.html", total=0, datas=[], page_count=0, m=row_count)

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
        "list.html", 
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


@application.route('/dynamicurl/<variable_name>/')
def DynamicUrl(variable_name):
    return str(variable_name)

# 상품 상세 조회 
@application.route("/view_detail/<name>/")
def view_item_detail(name):
    print("###name:", name)
    data = DB.get_item_byname(str(name))
    print("###data:", data)
    return render_template("detail.html", name=name, data=data)

# 로그인 조회 
@application.route("/login")
def login():
    return render_template("login.html")

<<<<<<< HEAD
=======
# 로그인 요청 
>>>>>>> ddcd93ab66b7c33b4d6a5e960985ea045d142e56
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

<<<<<<< HEAD
=======
# 로그아웃 
>>>>>>> ddcd93ab66b7c33b4d6a5e960985ea045d142e56
@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('view_list'))

<<<<<<< HEAD
=======
# 회원가입 조회 
>>>>>>> ddcd93ab66b7c33b4d6a5e960985ea045d142e56
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
<<<<<<< HEAD
    
@application.route('/page2')
def page2():
    return render_template('page2.html') #list 

@application.route('/page3')
def page3():
    return render_template('page3.html')

@application.route('/page4')
def page4():
    return render_template('page4.html')

@application.route('/page5')
def page5():
    return render_template('page5.html')

@application.route('/page6')
def page6():
    return render_template('page6.html')

@application.route('/page7')
def page7():
    return render_template('page7.html')

@application.route('/page8')
def page8():
    return render_template('page8.html')
=======
>>>>>>> ddcd93ab66b7c33b4d6a5e960985ea045d142e56

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)


