from contextlib import nullcontext
from flask import Flask, redirect,render_template, request
import mysql.connector
# import requests
db = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="password",
    database="social"
)

app = Flask(__name__)
@app.route('/',methods=['GET','POST'])
def Home():
    if request.method=='POST' :
        global name
        name=request.form['na']
        return redirect('/Posts')
    else:
        return render_template('index.html')

@app.route('/Posts',methods=['GET','POST'])
def Posts():
    if request.method=='POST':
        try:
            print("else part")
            query1=('INSERT INTO NewPost(user,post) VALUES(%s,%s)')
            query2=('INSERT INTO NewComment(postId,comment,user) VALUES(%s,%s,%s)')
            # query3=('select * from NewPost where post like '{}'')
            Uname=name
            if 'b2' in request.form:
                post=request.form['textBox']
                cursor=db.cursor()
                cursor.execute(query1,(Uname,post))
                db.commit()
            elif 'b1' in request.form:
                post=request.form['commentBox']

                poId=request.form['pid']
                cursor=db.cursor()
                cursor.execute(query2,(poId,post,Uname))
                db.commit()
            elif 'b3' in request.form:
                
                search=request.form['searchBar']
                # reSearch='%'+search+'%'
                cursor=db.cursor()
                
                cursor.execute("select * from NewPost where post like '{}'".format('%'+search+'%'))
                print('search')
                searchData=cursor.fetchall()
                
                return render_template('post.html',data=searchData)

                
            print('after')
            return redirect('/Posts')  
        except mysql.connector.Error as err:
            return f"An error occured: {err}"
    else:
        print('of part')
        try:
            cursor =db.cursor()
            query_table1 = "SELECT * FROM NewPost order by postId desc"
            cursor.execute(query_table1)
            post_table = cursor.fetchall()
            
            query_table2 = "SELECT *  FROM NewComment order by postId desc"
            cursor.execute(query_table2)
            comment_table = cursor.fetchall()

            return render_template('post.html', data=post_table, com=comment_table)
        except Exception as err:
            print('error')
            return f"An error occurred: {err}"
        

        
       