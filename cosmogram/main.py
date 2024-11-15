import datetime

from flask import Flask, render_template, request, send_from_directory, make_response
from flask import  Flask, render_template, request, redirect, url_for, flash, make_response, session
import MyFunc as mf
import settings as conf

app = Flask(__name__, template_folder=conf.GET("template"))
# app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)

# @app.route('/')
# def index():
#     return render_template('home.html')


@app.route('/', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        DATA = dict(request.form.to_dict())
        print(DATA)
        if mf.check_login_pass(login=DATA["login"], password=DATA["pass"], db=DATA["BD"]):
            session["user"] = mf.login_to_id_user(login=DATA["login"], db=DATA["BD"])
            session["BD"] = DATA["BD"]
            print(session.values())
            session.modified = True
            return render_template("index.html")
        else:
            return render_template("auth-login.html", DATA={"status": "Неверные данные", "BDs": mf.get_BDs()})
    if "user" in session.keys():
        return render_template("index.html")
    else:
        return render_template("auth-login.html", DATA={"status": "", "BDs": mf.get_BDs()})


@app.route('/register', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        DATA = dict(request.form.to_dict())
        print(DATA)
        if session.get("BD") + ".db" in mf.get_BDs():
            if not mf.register_user(login=DATA["login"], password=DATA["pass"], db=DATA["BD"]):
                return render_template("auth-register.html", DATA={"status": "Неверные данные", "BDs": mf.get_BDs()})
            # session["user"] = mf.login_to_id_user(login=DATA["login"], db=DATA["BD"])
            # session["BD"] = DATA["BD"]
            # print(session.values())
            # session.modified = True
            else:
                return render_template("index.html")

    if "user" in session.keys():
        return render_template("auth-login.html")
    else:
        return render_template("auth-register.html", DATA={"status": "", "BDs": mf.get_BDs()})

@app.route('/session/')
def updating_session():
    res = str(session.items())
    return res

@app.route('/session-out/')
def clear_session():
    session.clear()
    session.modified = True
    return str(session.values())
#
# @app.route('/<string:strin>', methods = ['GET'])
# def indexi(strin):
#     ot = {}
#     if request.method == 'GET':
#         ot = dict(request.args)
#         if ot != {}:
#             print(ot)
#     # ot['id'] = 1
#     try:
#         ot['id']
#     except:
#         ot['id'] = 1
#
#     if strin == 'friends':
#         ot = mf.Friends()
#     if strin == 'rating':
#         ot = mf.Rating()
#     if strin == 'profile':
#         ot = mf.Profile(ot['id'])#()
#     if strin == 'clubs':
#         ot = mf.Clubs()
#     if strin == 'club_detail':
#         ot = mf.Club_detail(ot['id'])
#     if strin == 'events':
#         ot = mf.Events()
#     if strin == 'event_detail':
#         ot = mf.Event_detail(ot['id'])
#     if strin == 'quests':
#         ot = mf.Quests()
#     if strin == 'quest_detail':
#         ot = mf.Quest_detail(ot['id'])
#     if strin == 'library':
#         try:
#             ot = mf.Library(ot['path'], ot['file'], id=1)
#         except:
#             ot = mf.Library('', '', id=1)
#
#     if strin == 'favicon.ico':
#         return ''
#     if strin == 'get_file':
#         ott = mf.Library(ot['path'], ot['file'], id=1)
#         return send_from_directory(ott + "/", ot['file'])

    # print("\nOT " + str(ot))
    # return render_template(''+strin+'.html', DATA=ot)


if __name__ == '__main__':
    app.run(debug=True, host=conf.GET("host"), port=conf.GET("port"))
