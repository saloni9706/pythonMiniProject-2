from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL
from flask_paginate import Pagination, get_page_parameter

#create a Flask application
#the argument to Flask is the name of the application's module
#since we are running our application in a single file, leave it as __name__
app=Flask(__name__)




app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'python_search_engine'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()
#relative path to the root of your application
@app.route('/')
def hello_world():
    return 'Hello World!'
@app.route('/search_engine',methods=['GET', 'POST'])
def search_engine(name=None):

    page = request.args.get(get_page_parameter(), type=int, default=1)
    table_name="crawler"
    param="%"
    cursor.execute("SELECT * from "+table_name+"")
    conn.commit()
    data = cursor.fetchall()
    # print(data)
    pagination = Pagination(page=page, total=len(data))
    
    if request.method == "POST":
        # print(request)
        search_keyword = request.form['search_content']
        page = request.args.get(get_page_parameter(), type=int, default=1)
        print(page,"...............")
        # search by author or book
        table_name="crawler"
        param="%"
        cursor.execute("select * from "+table_name+" where Title LIKE '"+param+search_keyword+param+"' OR Content LIKE '"+param+search_keyword+param+"'")

        conn.commit()
        data = cursor.fetchall()
        # print(data)
        pagination = Pagination(page=page, total=len(data))
        return render_template('search_engine.html', data=data,pagination=pagination,css_framework='foundation')
    return render_template('search_engine.html',data=data,pagination=pagination)
app.run(debug=True)