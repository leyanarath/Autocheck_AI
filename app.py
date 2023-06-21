from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

from parapharsing import *
import os
i=0
user=200
os.environ["FLASK_ENV"] = "development"
app = Flask(__name__)





@app.route("/", methods = ['GET'])
def index():

  return render_template("index.html")

@app.route("/login", methods = ['POST','GET'])
def login():
   return render_template("login.html")
@app.route("/stdvari", methods = ['POST','GET'])
def stdvari():
      usermail= request.args.get('email')
      password= request.args.get('password')
      print(password,usermail)
      conn =sqlite3.connect('autocheck.db')
      c=conn.cursor()
      if(conn):
          print("sucess")
      c.execute('SELECT * FROM loginstudent where email=(?)',(usermail,))
      account = c.fetchall()
      for check in account:
            #print(account)
            if (check[3]==usermail and check[2]==password):
                  return asheet()
            
      

      return render_template("login.html")
@app.route("/lteacher", methods = ['GET','POST'])
def login_teacher():
   return render_template("loginteacher.html")

@app.route("/anskey", methods = ['POST','GET'])
def akey():   
      return render_template("answerkey.html")  

@app.route("/answer", methods = ['POST','GET'])
def asheet():
      ans1 = request.form.get('qus') 
      global i
      print(ans1) 
      queryin(ans1)
      conn =sqlite3.connect('autocheck.db')
      c=conn.cursor()
      if(conn):
          print("sucess")
      #cur.execute ("CREATE TABLE IF NOT EXISTS res ({column_name} TEXT);")

      c.execute("SELECT question FROM questionp")
      
      qusestions=c.fetchall()[i]
      print(qusestions)
      conn.close()
      i=i+1
      return render_template("answersheet.html",questions=qusestions)  
def queryin(ans1):
      print(ans1)
      conn =sqlite3.connect('autocheck.db')
      c=conn.cursor()
      if(conn):
          print("sucess")
      c.execute("INSERT INTO ans(answer,qusid) VALUES (?,?)",(ans1,i))
      conn.commit()
      conn.close()
@app.route('/submit', methods=['POST','GET'])
def submit():
      
      Para(user)
      conn =sqlite3.connect('autocheck.db')
      c=conn.cursor()
      if(conn):
          print("sucess")
      c.execute("select * from mark where userid=(?)",(user,))
      table_data = c.fetchall()
      conn.close()
      return render_template("submit.html",table_data=table_data)
@app.route('/submit1', methods=['GET','POST'])
def submit1():
      
      mark = request.form.get('mark')
      qus = request.form.get('question')
      ans =  request.form.get('answer')
      print(mark,qus)
      conn =sqlite3.connect('autocheck.db')
      c=conn.cursor()
      if(conn):
          print("sucess")
      #cur.execute ("CREATE TABLE IF NOT EXISTS res ({column_name} TEXT);")

      c.execute("INSERT INTO questionp (question,answer,mark) VALUES (?,?,?)",(qus,ans,mark))
      conn.commit()

      conn.close()
     # return string1 
      return render_template("submit1.html",submit=qus)
@app.route('/result', methods=['GET','POST'])
def sresult():
     return render_template("result.html")
if __name__=="__main__":
    app.run(debug=True)
