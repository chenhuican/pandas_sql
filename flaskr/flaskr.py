#/usr/bin/env python
#coding:utf-8
from flask import Flask,render_template,session,escape,url_for
from flask import request,g,flash,abort,redirect
from contextlib import closing
import sqlite3

#配置文件
DATABASE = 'flaskr.db'
DEBUG = True
#secret_key是需要为了保持客户端的会话安全。明智地选择该键，使得它难以猜测，最好是尽可能复杂。
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

#这个方法用于在请求时打开一个连接，并且在交互式 Python shell 和脚本中也能使用。这对以后很方便
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	#@closing 如果一个对象没有实现上下文，我们就不能把它用于with语句。这个时候，可以用closing()来把该对象变为上下文对象
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read().decode())
		db.commit()
	print('db is created')

@app.before_request
def before_request():
	g.db = connect_db()

'''
所有我们的函数中需要数据库连接，因此在请求之前初始化它们，在请求结束后自动关闭他们就很有意义。

Flask 允许我们使用before_request()，after_request()和 teardown_request()装饰器来实现这个功能:
'''
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

