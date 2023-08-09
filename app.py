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

cur = cnt.cursor()

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
    cur.execute("SELECT name, username FROM member;")

    user_list = []
    for (name, username) in cur:
        user_list.append(username)
    print(user_list)
        
    name = request.form.get("name", "")
    account = request.form.get("account", "")
    password = request.form.get("password", "")

    if account in user_list:
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
    
    cur.execute(("SELECT name, username, password, id FROM member WHERE username='{}' and password = '{}' LIMIT 1;").format(account,password))
    row = cur.fetchone()
    
    if row !=None:
        name, username, password, id = row
        session["id"] = id 
        session["name"] = name
        session["account"] = username
        session["password"] = password
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
