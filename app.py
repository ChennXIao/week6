from flask import Flask
from flask import request
from flask import redirect
from flask import json
from flask import render_template
from flask import session
from flask import url_for
import mysql.connector 
from secret import secret 

secret_key = secret.get('key')
cnt = mysql.connector.connect(
    user='root', 
    password=secret_key,
    host='127.0.0.1',
    database='website', 
)

cur = cnt.cursor(dictionary=True)

app = Flask(
        __name__,
        static_folder="static",
        static_url_path="/") 

app.secret_key = "wrerw"

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/signup',methods=["POST"])
def ver():

    name = request.form.get("name", "")
    account = request.form.get("account", "")
    password = request.form.get("password", "")
    signup = ("SELECT * FROM member WHERE username = %s;")
    cur.execute(signup, (account,))
    newmember = cur.fetchone()

    if newmember!=None:
        return redirect("/error?message=帳號已被註冊")
    else:
        data = (name,account,password)
        add_data = ("INSERT INTO member(name,username,password)VALUES(%s,%s,%s);")
        cur.execute(add_data,data)
        cnt.commit()

        return render_template("index.html")

@app.route('/signin',methods=["POST"])
def mem():
    account = request.form.get("account", "")
    password = request.form.get("password", "")
    signin = ("SELECT name, username, password, id FROM member WHERE username= %s and password = %s LIMIT 1;")
    cur.execute(signin,(account,password))
    member = cur.fetchone()
    
    if member !=None:
        
        session["id"] = member["id"]
        session["name"] = member["name"]
        session["account"] = member["username"]
        session["password"] = member["password"]
        print(session)
        return redirect(url_for('member')) 
    else:
        return redirect("/error?message=請輸入正確的帳號密碼")

@app.route("/member")
def member():
    cur.execute("SELECT name, member_id,content FROM member INNER JOIN message ON member.id = message.member_id ORDER BY message.time DESC;")
    data = cur.fetchall()

    if "name" in session:
        name = session["name"]
        print(name)
        return render_template("member.html", user=name,text=data)
    else:
        return redirect(url_for('index'))

@app.route("/createMessage",methods=["POST"])
def message():

    id = session["id"]  
    text = request.form.get("text","")

    message = (id,text)
    add_message = ("INSERT INTO message(member_id,content)VALUES(%s,%s);")
    cur.execute(add_message,message)
    cnt.commit()
    return redirect(url_for('member'))

@app.route("/error")
def error():
    message = request.args.get("message", "")
    return render_template("error.html", message=message)
    
@app.route("/signout")
def out():
    session.clear()
    return redirect(url_for('index'))

app.run()

