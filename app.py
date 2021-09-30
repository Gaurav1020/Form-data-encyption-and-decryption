from flask import Flask, render_template, request, redirect
import os
from flask.helpers import url_for
app=Flask(__name__)

import time
import csv,sqlite3
import numpy as np
import pandas as pd
import shutil

import cryptography
from cryptography.fernet import Fernet

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
@app.route('/', methods=["GET","POST"])
def index():
    return render_template('index.html')




@app.route('/x', methods=["GET","POST"])
def x():
    conn=sqlite3.connect(pathdb)
    curr=conn.cursor()
    curr.execute("create table if not exists CollegeDetails (FullName text, RegistrationNumber text)")
    name=request.form['name']
    regno=request.form['rno']
    if(name!=None and regno!=None):
        print("XXXXXXXXXXXXXXXXXXXXXXXXX\n"+name+"\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        name=(fernet.encrypt(name.encode())).decode('utf-8')
        regno=(fernet.encrypt(regno.encode())).decode('utf-8')
        query="insert into CollegeDetails (FullName, RegistrationNumber) values ('"+name+"', '"+regno+"');"
        curr.execute(query)
    conn.commit();
    return redirect('/')





@app.route('/database',methods=["GET","POST"])
def allData():
    conn=sqlite3.connect(pathdb)
    curr=conn.cursor()
    query="select * from CollegeDetails;"
    curr.execute(query)
    vals=curr.fetchall()
    X=[]
    for val in vals:
        X.append([(fernet.decrypt(val[0].encode())).decode('utf-8'),(fernet.decrypt(val[1].encode())).decode('utf-8')])
        print((fernet.decrypt(val[0].encode())).decode('utf-8'))
    conn.commit();
    return render_template('database.html', vals=X)
if __name__ == "__main__":
        app.run(debug=True,port=8998)
        