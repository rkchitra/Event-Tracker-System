
#Python code for connecting front end to back end and executing queries and everything. 
from flask import Flask,render_template,request,url_for,flash,session,redirect
from flask_mysqldb import MySQL
import os

app=Flask(__name__)


#configure db
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='thebasicbenzene31'
app.config['MYSQL_DB']='project'
app.secret_key = os.urandom(24)

mysql=MySQL(app)


#Sign-Up Page
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
		temp=cur.execute("SELECT email from login where email=%s",(email,))
		if(temp>0) :
			return render_template('sign_up.html',mesg="",mesg2="Already exists")
		if(passwd!=passwd2):
			return render_template('sign_up.html', mesg="Passwords don't match!",mesg2="")
		else:	                                                                                                      
			cur.execute("INSERT INTO login(name,email,passwd) values(%s,%s,%s)",(name,email,passwd))
			mysql.connection.commit()
			cur.close()
			return render_template('success.html')
	return render_template('sign_up.html', mesg="",mesg2="")



#Home page for users(non-event handlers)
@app.route('/home',methods=['GET','POST'])
def home():
	if 'email' not in session :
		return redirect(url_for('index2'))
	if request.method=='POST' :
		session.pop('email',None)
		return '<h1>Logged Out </h1>'
	return render_template('home.html')


#Login Page
@app.route('/login',methods=['GET','POST'])

def index2():
	
	session.pop('email',None)
	if request.method=='POST' :
		#fetch login details
		user2=request.form
		global em
		em=user2['email']
		passwdd=user2['passwd']
		cur=mysql.connection.cursor()
		cur.execute("SELECT passwd FROM login where email=%s",(em,))
		p2=cur.fetchone()
		if p2 :
			if(p2[0]!=passwdd):
				return render_template('login.html',mesg="Invalid credentials entered")
			else :
				cur.execute("SELECT eh FROM login where email=%s",(em,))
				p2=cur.fetchone()
				session['email']=em
				if(p2[0]=='N'):
					return redirect(url_for('home'))
				else :
					return redirect(url_for('homee'))
		else :
			return render_template('login.html',mesg="Invalid credentials entered")	
		cur.close()
		
	return render_template('login.html',mesg="")


#On clicking the logout button, session is terminated
@app.route('/logout')

def logout():
	session.pop('email',None)
	return redirect(url_for('index2'))

#on successfully signing up	
@app.route('/success')

def success():
	return render_template('success.html')


#onyx page
@app.route('/onyx',methods=['GET','POST'])

def Onyx():
	if 'email' not in session :
		return redirect(url_for('index2'))
	else :
		return render_template('onyx.html')

#list of upcoming events 
@app.route('/events',methods=['GET','POST'])
def events():
	cur2=mysql.connection.cursor()
	cur2.execute("call update_events()") #calls procedure to ensure old events are deleted from this table and inserted into 'pevents'
	mysql.connection.commit()
	cur2.close()

	global indexing
	indexing=int(0)
	if request.method == 'POST' :
		val=request.form.getlist('filter_system')
		cur=mysql.connection.cursor()
		cur.execute("SELECT count(*) from events")
		no2=cur.fetchall() 
		cur.execute("SELECT * from events where big_event='yes' ORDER BY dt")
		cn=cur.fetchall()
		cur.execute("SELECT * from events where big_event='no' ORDER BY dt")
		cn2=cur.fetchall()
		x1=[[0]]

		x2=[]
		for i in cn :
			x2.append(i)
		for i in cn2 :
			x2.append(i)

		tuple(x2)

		cur.close()
		if val[0]=='All' :
			return render_template('disp2.html',no=no2,ev=x2,index=indexing,max=no2,tot=no2)
		else :		
			l2=[]
			str2=x2
			
			for i in str2 :
				if i[0] in val:
					x1[0][0]=x1[0][0]+1
					l2.append(i)
				
				tuple(l2)
				tuple(x1)
				#return render_template('sample.html',val1=cn)
			return render_template('disp2.html',no=x1,ev=l2,index=indexing,max=no2,tot=no2)
		
	else :
		cur=mysql.connection.cursor()
		cur.execute("SELECT count(*) from events")
		no2=cur.fetchall() 
		cur.execute("SELECT * from events where big_event='yes' ORDER BY dt")
		cn=cur.fetchall()
		cur.execute("SELECT * from events where big_event='no' ORDER BY dt")
		cn2=cur.fetchall()

		x2=[]
		for i in cn :
			x2.append(i)
		for i in cn2 :
			x2.append(i)

		tuple(x2)

		cur.close()
	return render_template('disp2.html',no=no2,ev=x2,index=indexing,max=no2,tot=no2)


#page that displays the previous events conducted in that academic year
@app.route('/pevents',methods=['GET','POST'])

def pevents():
	global indexing
	indexing=int(0)
	if request.method == 'POST' :
		val=request.form.getlist('filter_system')
		cur=mysql.connection.cursor()
		cur.execute("SELECT count(*) from pevents")
		no2=cur.fetchall() 
		cur.execute("SELECT * from pevents where big_event='yes' ORDER BY dt")
		cn=cur.fetchall()
		cur.execute("SELECT * from pevents where big_event='no' ORDER BY dt")
		cn2=cur.fetchall()
		x1=[[0]]

		x2=[]
		for i in cn :
			x2.append(i)
		for i in cn2 :
			x2.append(i)

		tuple(x2)

		cur.close()
		if val[0]=='All' :
			return render_template('disp.html',no=no2,ev=x2,index=indexing,max=no2,tot=no2)
		else :		
			l2=[]
			str2=x2
			
			for i in str2 :
				if i[0] in val:
					x1[0][0]=x1[0][0]+1
					l2.append(i)
				
				tuple(l2)
				tuple(x1)
				#return render_template('sample.html',val1=cn)
			return render_template('disp.html',no=x1,ev=l2,index=indexing,max=no2,tot=no2)
		
	else :
		cur=mysql.connection.cursor()
		cur.execute("SELECT count(*) from pevents")
		no2=cur.fetchall() 
		cur.execute("SELECT * from pevents where big_event='yes' ORDER BY dt")
		cn=cur.fetchall()
		cur.execute("SELECT * from pevents where big_event='no' ORDER BY dt")
		cn2=cur.fetchall()

		x2=[]
		for i in cn :
			x2.append(i)
		for i in cn2 :
			x2.append(i)

		tuple(x2
)
		cur.close()
	return render_template('disp.html',no=no2,ev=x2,index=indexing,max=no2,tot=no2)


#page to register for events
@app.route('/reg/<e__name>',methods=['GET','POST'])

def reg(e__name):

	if request.method=='POST' :
		events1=request.form
		sname=events1['name']
		usn=events1['usn']
		email=events1['email']
		mem=events1['member']
		ph=events1['phone']
		cur=mysql.connection.cursor()
		eve_name = e__name
		cur.execute("SELECT * from reg where ename=%s and usn=%s",(eve_name,usn))
		temp=cur.fetchall()
		if temp :

			return render_template('reg.html',e_name=e__name,check=int(-1))
		else :
			cur.execute("INSERT into reg values(%s,%s,%s,%s,%s,%s)",(eve_name,sname,usn,email,ph,mem))
			mysql.connection.commit()
		cur.close()

		

	return render_template('reg.html',e_name=e__name)


#home page for event handlers with the option of creating events
@app.route('/homee',methods=['GET','POST'])

def homee():
	if 'email' not in session :
		return redirect(url_for('index2'))
	else :
		return render_template('homee.html')


#events registered for by a student
@app.route('/sevents',methods=['GET','POST'])

def sevents():
	if 'email' not in session :
		return redirect(url_for('index2'))
	else :
		em=session['email']
		cur=mysql.connection.cursor()
		cur.execute("SELECT e.cname,r.ename,e.edescp,e.dt,e.big_event from reg r,events e where r.ename=e.ename and r.email=%s",(em,))
		par=cur.fetchall()
		cur.execute("SELECT e.cname,r.ename,e.edescp,e.dt,e.big_event from reg r,pevents e where r.ename=e.ename and r.email=%s",(em,))
		par2=cur.fetchall()
		cur.close()
		return render_template('sevents.html',ev=par,ev2=par2)

#creating an event page
@app.route('/create',methods=['GET','POST'])
def create():
	if 'email' not in session :
		return redirect(url_for('index2'))
	else :

		if request.method=='POST':
			#fetch form data
			user=request.form 
			name=user['ename']
			desc=user['edesc']
			seats=user['seats']
			dt=user['date']
			venn=user['venue']
			tm=user['time']
			op=user['options']
			cur=mysql.connection.cursor()
			cur.execute("SELECT name from login where email=%s",(em,))
			n2=cur.fetchone()
			cur.execute("INSERT INTO events(cname,ename,edescp,seats,dt,tm,venue,big_event) values(%s,%s,%s,%s,%s,%s,%s,%s)",(n2[0],name,desc,seats,dt,tm,venn,op))
			mysql.connection.commit()
			cur.close()
			return redirect(url_for('homee'))

		return render_template('create.html')
if __name__=='__main__':

	app.run(debug=True)


