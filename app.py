from flask import Flask , render_template, request
from data import Articles
from mysql import Mysql
import config
import pymysql

# print(Articles)

app = Flask(__name__)

mysql = Mysql(password=config.PASSWORD)

@app.route('/' , methods=['GET','POST'])
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
    
    return render_template('index.html')

""" @app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == "GET":
        return render_template('hello.html')
    
    elif request.method == "POST":
        name = request.form['name']
        hello = request.form['hello']
        return render_template('index.html', name = name, hello = hello) """
    
""" @app.route('/list', methods=['GET', 'POST'])
def list():
    data = Articles()
    return render_template('list.html', data = data ) """

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
            return "Persistance Denied"
        else:
            result = mysql.insert_user(username, email, phone, password)
            print(result)
            return "success"
    
    elif request.method == "GET":
        return render_template('register.html')   
    
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
            return str(rows[0][0])
        else:            
            return "User is Not Founded"
                    

if __name__ == '__main__':
    app.run(debug=True)