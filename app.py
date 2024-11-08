from flask import Flask, render_template

application  = Flask(__name__)

@application.route('/')
def home():
    return render_template('page1.html')

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)