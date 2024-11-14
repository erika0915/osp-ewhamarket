from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import sys 

application  = Flask(__name__)
DB = DBhandler()

@application.route("/")
def hello() :
    return render_template("index.html")

@application.route('/reg_items')
def reg_items():
    return render_template('reg_items.html')

@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():

    image_file = request.files["file"]

    image_file.save("static/images/{}".format(image_file.filename))
    data = request.form 
    print(request.form)
    DB.insert_item(data['productName'], data, image_file.filename)
    return render_template("submit_item_result.html", data=data, img_path = "static/images/{}".format(image_file.filename))
    #reg_items

@application.route("/login")
def login():
    return render_template("login.html")

@application.route("/signup")
def signup():
    return render_template("signup.html")

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

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)