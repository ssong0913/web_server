from flask import Flask , render_template, request, redirect, session, url_for
from data import Articles
from mysql import Mysql
import config
import pymysql
from datetime import timedelta
from functools import wraps

# print(Articles)

app = Flask(__name__)

app.secret_key = "eungok"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=5)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'

mysql = Mysql(password=config.PASSWORD)

# 로그인 유지
def is_loged_in(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'is_loged_in' in session:
            return func(*args, **kwargs)
        else:
            return redirect('/login')
    return wrap

@app.route('/' , methods=['GET','POST'])
# @is_loged_in
def index():
    """ if request.method == "GET":
        os_info = dict(request.headers)
        print(os_info)
        name = request.args.get("name")
        print(name)
        hello = request.args.get("hello")
        print(hello)
        return render_template('index.html', header = f'{name}님 {hello}!!')
                #jinja2 문법
    elif request.method == "POST":
        data = request.form.get("name")
        data_2 = request.form['hello']
        print(f'{name}님 {hello}!!')
        return render_template('index.html', header = "안녕하세요adsfasdf") """
    # print(session['is_loged_in'])
    return render_template('index.html')

""" @app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == "GET":
        return render_template('hello.html')
    
    elif request.method == "POST":
        name = request.form['name']
        hello = request.form['hello']
        return render_template('index.html', name = name, hello = hello) """

@app.route('/list', methods=['GET', 'POST'])
def list():
    if request.method == "GET":
        # data = Articles()
        result = mysql.get_data()
        print(result)
        return render_template('list.html', data = result )
    
    elif request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        author = request.form['author']
        result = mysql.insert_list(title, desc, author)
        print(result)
        return redirect('/list')
    
@app.route('/create_list')
def create_list():    
        return render_template('dashboard.html')
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        # form[], form.get()
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        print(username, email, phone, password)
        
        
        db = pymysql.connect(host=mysql.host, user=mysql.user, db=mysql.db, password=mysql.password, charset=mysql.charset)
        curs = db.cursor()

        sql = f'SELECT * FROM user WHERE email = %s;'

        curs.execute(sql, email) 

        rows = curs.fetchall()
        print(rows)

        if rows:

            return render_template('register.html', data=1)
        else:
            result = mysql.insert_user(username, email, phone, password)
            print(result)
            return redirect('/login')
    
    elif request.method == "GET":
        return render_template('register.html', data=0)   
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    
    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        db = pymysql.connect(host=mysql.host, user=mysql.user, db=mysql.db, password=mysql.password, charset=mysql.charset)
        curs = db.cursor()

        sql = f'SELECT * FROM user WHERE email = %s;'

        curs.execute(sql, email) 

        rows = curs.fetchall()
        print(rows)

        if rows:
            result = mysql.verify_password(password, rows[0][4])
            if result:
                session['is_loged_in'] = True
                session['username'] = rows[0][1]
                return redirect('/')
                # return render_template('index.html', is_loged_in = session['is_loged_in'], user=session['username'])
            else:
                return redirect('/login')
        else:            
            return render_template('login.html')
        
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/edit/<ids>' , methods=['GET', 'POST'])
def edit(ids):
    if request.method == 'GET':        
        db = pymysql.connect(host=mysql.host, user=mysql.user, db=mysql.db, password=mysql.password, charset=mysql.charset)
        curs = db.cursor()

        sql = f'SELECT * FROM list WHERE `id` = %s;'

        curs.execute(sql, ids)
        rows = curs.fetchall()
        print(rows)
        db.close()
        return render_template('list_edit.html', data = rows)
    
    elif request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        author = request.form['author']
        
        result = mysql.update_list(ids, title, desc, author)
        print(result)
        return redirect('/list')

@app.route('/delete/<ids>', methods=['GET', 'POST'])
def delete(ids):
    result = mysql.delete_list(ids)
    print(result)
    return redirect('/list')

                    

if __name__ == '__main__':
    app.config['SECRET_KEY']='engok'
    app.run(debug=True)