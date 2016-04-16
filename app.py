from mongoengine import *
from flask import *
from users import User
import os
from flask.ext.login import LoginManager, login_required, login_user


# Upload data to Mongo
connect('nim', host='mongodb://hiep:hiepxanh@ds015929.mlab.com:15929/nim')


class Lecture(Document):
    href = StringField()
    title = StringField()
    brief = ListField(StringField())
    document = ListField(DictField())
    assignment = ListField(DictField())
    edit = StringField()


class Users(Document):
    username = StringField()
    password = StringField()

# user1 = Users(username = "dvquy",
#               password = "dvquy123")
# user2 = Users(username = "ntnhan",
#               password = "ntnhan123")
# user2.save()
# user1.save()

login_manager = LoginManager()
app = Flask(__name__)
app.secret_key = 'Why should I tell you my secret key?'

lecturelist = Lecture.objects
for lecture in lecturelist:
    print(lecture.edit)

login_manager.init_app(app)

@login_manager.user_loader
def user_loader(user_id):
    return User()


@app.route('/', methods=['GET', 'POST'])
def login():
    user_list = Users.objects
    error = ""
    try:
        if request.method == "POST":
            u = request.form['username']
            p = request.form['password']
            for user in user_list:
                if user.username == u and user.password == p:
                    user = User()
                    login_user(user, remember=False)
                    return redirect(url_for("index"))
            error = "Invalid credentials. Please try again!"

    except Exception as e:
        flash(e)
        return render_template("login.html", error=error)

    return render_template('login.html', error=error)


@app.route('/<lectureHref>/', methods= ['GET', 'POST'])
@login_required
def lectureHref(lectureHref):
    lecture_list = Lecture.objects
    for lecture in lecture_list:
        if lecture.href == lectureHref:
            if request.method == "POST":
                u = request.form['update']
                for brief in lecture.brief:
                    if u == brief:
                        lecture_brief = lecture.brief
                        lecture_brief.remove(u)
                        lecture.save()
                        return render_template("lecture.html",
                                   lecture=lecture,
                                   lecture_list=lecture_list)

                lecture_brief = lecture.brief
                lecture_brief.append(u)
                lecture.save()
            return render_template("lecture.html",
                                   lecture=lecture,
                                   lecture_list=lecture_list)


# Lay anh tai local host:
@app.route('/<path:path>/')
def static_file(path):
    return app.send_static_file(path)

@app.route('/index/')
@login_required
def index():
    lecture_list = Lecture.objects
    return render_template("Index.html",
                           lecture_list=lecture_list)


# Errors handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.errorhandler(401)
def unauthorized_access(e):
    return render_template("401.html")


@app.errorhandler(500)
def unauthorized_access(e):
    return render_template("500.html")


# Upload files
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/upload", methods=['POST'])
@login_required
def upload():
    target = os.path.join(APP_ROOT, 'baitap/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "".join([target, filename])
        print(destination)
        file.save(destination)

    return render_template("upload complete.html")

# @app.route('/lecture1-edit/')
# def lecture1_edit():
#     return render_template("lecture-edit.html")

# @app.route('/index/<lectureEdit>', methods=['GET', 'POST'])
# @login_required
# def lectureEdit(lectureEdit):
#     lecture_list = Lecture.objects
#     for lecture in lecture_list:
#         if lecture.edit == lectureEdit:
#             if request.method == "POST":
#                 upd = request.form["update"]
#                 lecture.brief.append(upd)
#                 lecture.save()
#
#             return render_template("lecture-edit.html",
#                                    lecture=lecture)

if __name__ == '__main__':
    app.run()



