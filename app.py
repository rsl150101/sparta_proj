import pymysql
from flask import Flask, render_template, request, flash, session, redirect, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "db_codescanner"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    flash("로그아웃 되었습니다.")
    session['login_flag'] = False
    session['user_id'] = ""
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/profile', methods=['GET'])
def profile():
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='dbgosu11!!', db='test',
                         charset='utf8')
    cursor = db.cursor()
    user_id = session['user_id']
    sql = """
        SELECT user_id, name, email FROM users
        where user_id = (%s)
    """
    cursor.execute(sql, user_id)
    result = cursor.fetchone()
    db.commit()
    db.close()

    user_name = result[1]
    user_email = result[2]
    return render_template('my_profile.html', d1=user_id, d2=user_name, d3=user_email )

@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='dbgosu11!!', db='test',
                         charset='utf8')
    cursor = db.cursor()
    user_id = session['user_id']
    sql = """
        SELECT user_id, name, email FROM users
        where user_id = (%s)
    """
    cursor.execute(sql, user_id)
    result = cursor.fetchone()
    db.commit()
    db.close()

    user_name = result[1]
    user_email = result[2]

    if request.method == "POST":
        details = request.form
        user_name_form = details['user_name']
        user_pw_form = details['user_pw']
        pw_confirm = details['pw_confirm']

        if user_pw_form == pw_confirm:
            db = pymysql.connect(host='localhost', port=3306, user='root', passwd='dbgosu11!!', db='test',
                                 charset='utf8')
            cursor = db.cursor()
            sql = """
                UPDATE users
                SET name = (%s), user_pw = (%s)
                WHERE user_id = (%s)
            """
            cursor.execute(sql, (user_name_form, user_pw_form, user_id))

            sql = """
                    SELECT user_id, name, email FROM users
                    where user_id = (%s)
                """
            cursor.execute(sql, user_id)
            result = cursor.fetchone()
            db.commit()
            db.close()
            user_name = result[1]
            user_email = result[2]
        else:
            flash("새 비밀번호와 비밀번호 확인이 일치하지 않습니다")

    return render_template('edit_profile.html', d1=user_id, d2=user_name, d3=user_email )

@app.route('/profile/delete', methods=['GET', 'POST'])
def delete_page():
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='dbgosu11!!', db='test',
                         charset='utf8')
    cursor = db.cursor()
    user_id = session['user_id']
    sql = """
        SELECT user_id, name, email, user_pw FROM users
        where user_id = (%s)
    """
    cursor.execute(sql, user_id)
    result = cursor.fetchone()
    db.commit()
    db.close()
    user_name = result[1]
    user_email = result[2]
    user_pw = result[3]

    if request.method == "POST":
        user_pw_form = request.form['user_pw']
        if user_pw == user_pw_form:
            db = pymysql.connect(host='localhost', port=3306, user='root', passwd='dbgosu11!!', db='test',
                                 charset='utf8')
            cursor = db.cursor()
            sql = """
                DELETE FROM users
                WHERE user_id = (%s) AND user_pw = (%s)
            """
            cursor.execute(sql, (user_id, user_pw_form))
            db.commit()
            db.close()
            session['login_flag'] = False
            session['user_id'] = ""
            return render_template('index.html')
        else:
            flash("비밀번호가 일치하지 않습니다")
    return render_template('delete_account.html', d1=user_id, d2=user_name, d3=user_email )

# @app.route('/delete_done', methods=['POST'])
# def delete_account():
#     if request.method == "POST":
#         db = pymysql.connect(host='localhost', port=3306, user='root', passwd='dbgosu11!!', db='test',
#                              charset='utf8')
#         cursor = db.cursor()
#         details = request.form
#         user_id = details['user_id']
#         user_pw = details['user_pw']
#         sql = """
#             DELETE FROM users
#             WHERE user_id = (%s) AND user_pw = (%s)
#         """
#         cursor.execute(sql, (user_id, user_pw))
#         db.commit()
#         db.close()
#         session['login_flag'] = False
#         session['user_id'] = ""
#         return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='dbgosu11!!', db='test',
                             charset='utf8')
        cursor = db.cursor()

        details = request.form
        user_id = details['user_id']
        user_pw = details['user_pw']
        pw_confirm = details['pw_confirm']
        name = details['name']
        email = details['email']
        sql = """
             SELECT * FROM users
             where user_id = (%s)
        """
        cursor.execute(sql, user_id)
        id_check_result = cursor.fetchone()
        if id_check_result != None:
            db.commit()
            db.close()
            flash("이미 가입된 아이디입니다. 다른 아이디를 선택하세요.")
            return render_template('register.html')
        else:
            sql = """
                SELECT * FROM users
                where email = (%s)
            """
            cursor.execute(sql, email)
            email_check_result = cursor.fetchone()
            if email_check_result != None:
                db.commit()
                db.close()
                flash("이미 가입된 이메일 입니다.")
                return render_template('register.html')
            elif user_pw == pw_confirm:
                sql = """
                    INSERT INTO 
                    users(
                        user_id
                        , user_pw
                        , name
                        , email
                        ) 
                        VALUES 
                        (%s, %s, %s, %s)
                """
                cursor.execute(sql, (user_id, user_pw, name, email))
                db.commit()
                db.close()
                flash("회원가입이 완료되었습니다.")
                return render_template('login.html')
            else:
                db.commit()
                db.close()
                flash("비밀번호 확인이 일치하지 않습니다.")
                return render_template('register.html')
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def signin():
    if request.method == 'POST':
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='dbgosu11!!', db='test',
                             charset='utf8')
        cursor = db.cursor()
        details = request.form
        user_id = details['user_id']
        user_pw = details['user_pw']
        if len(user_id) == 0 or len(user_pw) ==0:
            flash("아이디 혹은 비밀번호가 입력되지 않았습니다.")
            return render_template('login.html')
        else:
            sql = """
                SELECT user_id, user_pw, name FROM users
                where user_id = (%s)
            """
            cursor.execute(sql, user_id)
            user_in_db = cursor.fetchone()

            if user_in_db == None:
                flash("존재하지 않는 아이디입니다.")
                db.commit()
                db.close()
                return render_template('login.html')
            elif user_pw == user_in_db[1]:
                user_name = user_in_db[2]
                session['login_flag'] = True
                session['user_id'] = user_id
                message = "{}님 환영합니다!".format(user_name)
                flash(message)
                db.commit()
                db.close()
                return render_template('index.html')
            else:
                flash("잘못된 비밀번호를 입력하셨습니다.")
                db.commit()
                db.close()
                return render_template('login.html')

    return render_template('login.html')

if __name__ == '__main__':
    app.run()
