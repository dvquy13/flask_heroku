from flask import *

app = Flask(__name__)

@app.route('/')
def lecture_1_edit():
    return render_template("lecture-edit.html")

if __name__ == '__main__':
    app.run()