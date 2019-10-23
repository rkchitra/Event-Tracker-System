from flask import Flask,render_template,request,url_for
from flask_mysqldb import MySQL

app=Flask(__name__)

#configure db
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='thebasicbenzene31'
app.config['MYSQL_DB']='project'

mysql=MySQL(app)

@app.route('/',methods=['GET','POST'])

def index():
	if request.method=='POST':
		#fetch form data
		user=request.form 
		name=user['name']
		email=user['email']
		passwd=user['passwd']
		passwd2=user['passwd2']
		cur=mysql.connection.cursor()
		if(passwd!=passwd2):
			return render_template('sign_up.html', mesg="Passwords don't match!")
		else:	                                                                                                      
			cur.execute("INSERT INTO login(name,email,passwd) values(%s,%s,%s)",(name,email,passwd))
			mysql.connection.commit()
			cur.close()
			return render_template('success.html')
	return render_template('sign_up.html', mesg="")

@app.route('/login',methods=['GET','POST'])

def index2():
	if request.method=='POST' :
		#fetch login details
		user2=request.form
		em=user2['email']
		passwdd=user2['passwd']
		cur=mysql.connection.cursor()
		cur.execute("SELECT passwd FROM login where email=%s",(em,))
		p2=cur.fetchone()
		if(p2[0]!=passwdd):
			return render_template('login.html',mesg="Invalid credentials entered")
		else :
			return '<h2>Logged in!</h2>'
		cur.close()
	return render_template('login.html',mesg="")

@app.route('/success')

def success():
	return render_template('success.html')

if __name__=='__main__':
	app.run(debug=True)


