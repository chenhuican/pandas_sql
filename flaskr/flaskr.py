#/usr/bin/env python
#coding:utf-8
from flask import Flask,render_template,session,escape,url_for
from flask import request,g,flash,abort,redirect
from contextlib import closing
import sqlite3

#配置文件
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'xffgffg'
USERNAME = 'admin'
PASSWORD = '123456'

#创建应用
app = Flask(__name__)
app.config.from_object(__name__)

#from_object()将会寻找给定的对象(如果它是一个字符串，则会导入它)， 
#搜寻里面定义的全部大写的变量。在我们的这种情况中，配置文件就是我们上面写的几行代码。 
#你也可以将他们分别存储到多个文件


#app.config.from_envvar('FLASKR_SETTINGS',silent=True)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read().decode())
		db.commit()
	print('db is created')

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	g.db.close()

@app.route('/')
def show_entries():
	cur = g.db.execute('select title,text from entries order by id desc')
	entries = [dict(title=row[0],text=row[1]) for row in cur.fetchall()]
	return render_template('show_entries.html',entries=entries)

@app.route('/add',methods=['POST'])
def add_entry():
	if not session.get('login_in'):
		abort(401)
	g.db.execute('insert into entries(title,text) values(?,?) ',[request.form['title'],request.form['text']])
	g.db.commit()
	flash('add new entries ok!')
	return redirect(url_for('show_entries'))

@app.route('/login',methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] !=app.config['USERNAME']:
			error ='Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['login_in'] = True
			flash('You were logged_in')
			return redirect(url_for('show_entries'))
	return render_template('login.html',error=error)

@app.route('/logout')
def logout():
	session.pop('login_in',None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))

if __name__ == '__main__':
	app.run()

