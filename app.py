from flask import Flask, render_template

application  = Flask(__name__)

@application.route('/page1')
def page1():
    return render_template('page1.html')

@application.route('/page2')
def page2():
    return render_template('page2.html')

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