from flask import Flask, render_template, request, redirect
import os
from flask.helpers import url_for
app=Flask(__name__)
import json
import time
import csv,sqlite3
import numpy as np
import pandas as pd
import shutil
import numpy as np
import cryptography
from cryptography.fernet import Fernet
import time
# key=Fernet.generate_key()
# print("Key=",key)
# file=open('key.key', 'wb')
# file.write(key)
# file.close()
file = open('key.key', 'rb') # rb = read bytes
key  = file.read()
file.close()
# print (key)
fernet=Fernet(key)

path=os.getcwd()
# print(path)
pathdb=path+"/dadb.db"

etemp = []  
flag=-1
dtemp = [] 
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sign-out')
def sign_out():
    global flag
    global dtemp
    global etemp
    dtemp=[]
    etemp=[]
    flag=-1
    print(flag)
    return redirect('/')



@app.route('/sign-in', methods=["GET","POST"])
def sign_in():
    return render_template('sign-in.html')

@app.route('/sign-up', methods=["GET","POST"])
def sign_up():
    return render_template('sign-up.html')


@app.route('/sign-up-send', methods=["GET","POST"])
def encrypt_send_su():
    conn=sqlite3.connect(pathdb)
    curr=conn.cursor()
    regno=request.form['regno']
    pwd=request.form['pwd']
    query="select RegistrationNumber, Password from CollegeDetails;"
    curr.execute(query)
    vals=curr.fetchall()
    for val in vals:
        if (regno==fernet.decrypt(val[0].encode()).decode('utf-8')):
            if (pwd==fernet.decrypt(val[1].encode()).decode('utf-8')):
                query="select FullName, RegistrationNumber, DOB, Address, PhoneNumber from CollegeDetails where RegistrationNumber = '" + val[0] +"' ;"
                curr.execute(query)
                vex=curr.fetchone()
                global etemp
                global flag
                flag=1
                etemp=vex
                print(flag)
                return redirect('/eprofile')
            else:
                break
    print("Incorrect username or password")
    return redirect('/sign-up')


@app.route('/eprofile', methods=["GET","POST"])
def eprofile():
    return render_template('/eprofile.html', A=etemp)


@app.route('/dprofile', methods=["GET","POST"])
def dprofile():
    return render_template('/dprofile.html', A=dtemp)


@app.route('/decrypt', methods=["GET","POST"])
def decrypt():
    conn=sqlite3.connect(pathdb)
    curr=conn.cursor()
    regno=request.form['regno']
    query="select FullName, RegistrationNumber, DOB, Address, PhoneNumber from CollegeDetails where RegistrationNumber = '" + regno +"' ;"
    curr.execute(query)
    res=curr.fetchone()
    global dtemp
    global flag
    dtemp=[]
    
    for val in res:
        flag=0
        dtemp.append(fernet.decrypt(val.encode()).decode('utf-8'))
    # print(X)
    print(flag)
    # print(dtemp)
    return redirect('/dprofile')


@app.route('/encrypt-send', methods=["GET","POST"])
def encrypt_send():
    conn=sqlite3.connect(pathdb)
    curr=conn.cursor()
    curr.execute("create table if not exists CollegeDetails (FullName text, RegistrationNumber text, Password text, DOB text, Address text, PhoneNumber text)")
    name=request.form['name']
    regno=request.form['rno']
    pwd=request.form['pwd']
    date=request.form['date']
    addr=request.form['addr']
    phone=request.form['phone']
    query="select RegistrationNumber from CollegeDetails;"
    curr.execute(query)
    vals=curr.fetchall()
    for val in vals:
        print(val)
        if (regno==fernet.decrypt(val[0].encode()).decode('utf-8')):
            return redirect('/sign-in')
    if(name!=None and regno!=None):
        name=(fernet.encrypt(name.encode())).decode('utf-8')
        regno=(fernet.encrypt(regno.encode())).decode('utf-8')
        pwd=(fernet.encrypt(pwd.encode())).decode('utf-8')
        date=(fernet.encrypt(date.encode())).decode('utf-8')
        addr=(fernet.encrypt(addr.encode())).decode('utf-8')
        phone=(fernet.encrypt(phone.encode())).decode('utf-8')
        query="insert into CollegeDetails (FullName, RegistrationNumber, Password, DOB, Address, PhoneNumber) values ('"+name+"', '"+regno+"', '"+pwd+"','"+date+"', '"+addr+"', '"+phone+"');"
        curr.execute(query)
    conn.commit()
    return redirect('/')


@app.route('/update-profile', methods=["GET","POST"])
def update_profile():
    global flag
    global etemp
    global dtemp
    dtemp=[]
    if not etemp:
        return redirect('/sign-up')
    else:
        for val in etemp:
            flag=0
            dtemp.append(fernet.decrypt(val.encode()).decode('utf-8'))
        return render_template('update.html', A=dtemp)


@app.route('/update', methods=["GET","POST"])
def update():
    global flag
    global etemp
    global dtemp
    dtemp=[]
    regno = etemp[1]
    
    for val in etemp:
        flag=0
        dtemp.append(fernet.decrypt(val.encode()).decode('utf-8'))
    etemp=[]
    conn=sqlite3.connect(pathdb)
    curr=conn.cursor()
    curr.execute("create table if not exists CollegeDetails (FullName text, RegistrationNumber text, Password text, DOB text, Address text, PhoneNumber text)")
    name=request.form['name']
    addr=request.form['addr']
    phone=request.form['phone']
    name=(fernet.encrypt(name.encode())).decode('utf-8')
    # regno=(fernet.encrypt(regno.encode())).decode('utf-8')
    # pwd=(fernet.encrypt(pwd.encode())).decode('utf-8')
    # date=(fernet.encrypt(date.encode())).decode('utf-8')
    addr=(fernet.encrypt(addr.encode())).decode('utf-8')
    phone=(fernet.encrypt(phone.encode())).decode('utf-8')
    query="update CollegeDetails SET FullName = '"+name+"' , Address = '"+addr+"', PhoneNumber = '"+phone +"' WHERE RegistrationNumber = '"+regno+"';"
    curr.execute(query)
    query="select FullName, RegistrationNumber, DOB, Address, PhoneNumber from CollegeDetails where RegistrationNumber = '" + regno +"' ;"
    curr.execute(query)
    res=curr.fetchone()
    conn.commit()
    for val in res:
        print(val)
        etemp.append(val)
    return redirect('/eprofile')


@app.route('/database',methods=["GET","POST"])
def allData():
    conn=sqlite3.connect(pathdb)
    curr=conn.cursor()
    query='select * from CollegeDetails;'
    print(query)
    curr.execute(query)
    vals=curr.fetchall()
    X=[]
    for val in vals:
        X.append([(fernet.decrypt(val[0].encode())).decode('utf-8'),(fernet.decrypt(val[1].encode())).decode('utf-8')])
        print((fernet.decrypt(val[0].encode())).decode('utf-8'))
    conn.commit();
    return render_template('database.html', data_pipeline=X)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
if __name__ == "__main__":
        app.run(debug=True,port=8998)

