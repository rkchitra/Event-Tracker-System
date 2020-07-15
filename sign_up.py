
#Python code for connecting front end to back end and executing queries and everything. 
from flask import Flask,render_template,request,url_for,flash,session,redirect
from flask_mysqldb import MySQL
import os
from flask_jsglue import JSGlue
from flask_mail import Mail, Message

app=Flask(__name__)
jsglue = JSGlue(app)
mail=Mail(app)

#configure mail details
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'acs.nie1234@gmail.com'
app.config['MAIL_PASSWORD'] = 'nieevent'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

global em

#configure db
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='xyz'
app.config['MYSQL_DB']='project'
app.secret_key = os.urandom(24)

mysql=MySQL(app)


#Sign-Up Page
@app.route('/',methods=['GET','POST'])

def index():
	if 'email' in session :
		return redirect(url_for('red_home'))
	if request.method=='POST':
		#fetch form data
		user=request.form 
		name=user['name']
		email=user['email']
		usn = user['usn']
		pno = user['pno']
		passwd=user['passwd']
		passwd2=user['passwd2']
		cur=mysql.connection.cursor()
		temp=cur.execute("SELECT email from login where email=%s or usn=%s",(email,usn,))
		if(temp>0) :
			return render_template('sign_up.html',mesg="This USN or email is already registered.",mesg2="")
		if(passwd!=passwd2):
			return render_template('sign_up.html', mesg="Passwords don't match!",mesg2="")
		else:	                                                                                                      
			cur.execute("INSERT INTO login(name,email,usn,pno,passwd) values(%s,%s,%s,%s,%s)",(name,email,usn,pno,passwd))
			mysql.connection.commit()
			cur.close()
			session['email']=email
			session['eh']='N'
			em=email
			return redirect(url_for('home'))
	return render_template('sign_up.html', mesg="",mesg2="")



#Home page for users(non-event handlers)
@app.route('/home',methods=['GET','POST'])
def home():
	if 'email' not in session :
		return redirect(url_for('index2'))
	return render_template('home.html',eh=session['eh'])


#Login Page
@app.route('/login',methods=['GET','POST'])

def index2():
	if 'email' in session :
		session.pop('email',None)
		session.pop('eh',None)
	if request.method=='POST' :
		#fetch login details
		user2=request.form
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
					session['eh']='N'
					return redirect(url_for('home'))
				else :
					session['eh']='Y'
					return redirect(url_for('homee'))
		else :
			return render_template('login.html',mesg="Invalid credentials entered")	
		cur.close()
		
	return render_template('login.html',mesg="")


@app.route('/red_home')

def red_home():
	if 'email' not in session :
		return redirect(url_for('index2'))
	if session['eh']=='N' :
		return redirect(url_for('home'))
	
	return redirect(url_for('homee'))


#On clicking the logout button, session is terminated
@app.route('/logout')

def logout():
	session.pop('email',None)
	session.pop('eh',None)
	return redirect(url_for('index2'))

def notif_check(club_name) :
	cursor=mysql.connection.cursor()
	count=cursor.execute("SELECT * from notify where email=%s and cname=%s",(session['email'],club_name,))
	cursor.close()
	if count == 0 :
		return -1
	return 1
@app.route('/notif2/<subs>/<clubname>',methods=['GET','POST'])
def notif2(subs,clubname) :
	cur=mysql.connection.cursor()
	if subs == 'subs' :
		cur.execute("INSERT into notify values (%s,%s)",(session['email'],clubname,))
		mysql.connection.commit()
	else :
		cur.execute("DELETE from notify where email=%s and cname=%s",(session['email'],clubname,))
		mysql.connection.commit()
	cur.close()
	if clubname == 'Force Ikshvaku' :
		return redirect(url_for('force_i'))
	return redirect(url_for(clubname))



#onyx page
@app.route('/Onyx',methods=['GET','POST'])

def Onyx():
	if 'email' not in session :
		return redirect(url_for('index2'))
	else :
		clubname='Onyx'
		cur=mysql.connection.cursor()
		cur.execute("SELECT * from events where cname=%s",(clubname,))
		eves=cur.fetchall()
		check=notif_check(clubname)
		if check == 1 :
			return render_template('onyx.html',subs="true",ev=eves)
		return render_template('onyx.html',subs="false",ev=eves)

#IEEE page
@app.route('/IEEE',methods=['GET','POST'])
def IEEE():
	if 'email' not in session :
		return redirect(url_for('index2'))
	else :
		clubname='IEEE'
		cur=mysql.connection.cursor()
		cur.execute("SELECT * from events where cname=%s",(clubname,))
		eves=cur.fetchall()
		check=notif_check(clubname)
		if check == 1 :
			return render_template('ieee.html',subs="true",ev=eves)
		return render_template('ieee.html',subs="false",ev=eves)

#Force Ikshvaku Page
@app.route('/force_i',methods=['GET','POST'])
def force_i():
	if 'email' not in session :
		return redirect(url_for('index2'))
	else :
		clubname='Force Ikshvaku'
		cur=mysql.connection.cursor()
		cur.execute("SELECT * from events where cname=%s",(clubname,))
		eves=cur.fetchall()
		check=notif_check(clubname)
		if check == 1 :
			return render_template('force_i.html',subs="true",ev=eves)
		return render_template('force_i.html',subs="false",ev=eves)
#ISSA Page
@app.route('/ISSA',methods=['GET','POST'])
def ISSA():
	if 'email' not in session :
		return redirect(url_for('index2'))
	else :
		clubname='ISSA'
		cur=mysql.connection.cursor()
		cur.execute("SELECT * from events where cname=%s",(clubname,))
		eves=cur.fetchall()
		check=notif_check(clubname)
		if check == 1 :
			return render_template('issa.html',subs="true",ev=eves)
		return render_template('issa.html',subs="false",ev=eves)
#UCSP Page
@app.route('/UCSP',methods=['GET','POST'])
def UCSP():
	if 'email' not in session :
		return redirect(url_for('index2'))
	else :
		clubname='UCSP'
		cur=mysql.connection.cursor()
		cur.execute("SELECT * from events where cname=%s",(clubname,))
		eves=cur.fetchall()
		check=notif_check(clubname)
		if check == 1 :
			return render_template('ucsp.html',subs="true",ev=eves)
		return render_template('ucsp.html',subs="false",ev=eves)

#list of upcoming events 
@app.route('/events',methods=['GET','POST'])
def events():
	if 'email' not in session :
		return redirect(url_for('index2'))
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
		if len(val)==0 or val[0]=='All' :
			return render_template('disp2.html',no=no2,ev=x2,index=indexing,max=no2,tot=no2,list1=['All'])
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
			return render_template('disp2.html',no=x1,ev=l2,index=indexing,max=no2,tot=no2,list1=val)
		
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
	l1=['All']
	return render_template('disp2.html',no=no2,ev=x2,index=indexing,max=no2,tot=no2,list1=l1)


#page that displays the previous events conducted in that academic year
@app.route('/pevents',methods=['GET','POST'])

def pevents():
	if 'email' not in session :
		return redirect(url_for('index2'))
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
		if len(val) == 0 or val[0]=='All' :
			return render_template('disp.html',no=no2,ev=x2,index=indexing,max=no2,tot=no2,list1=val)
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
			return render_template('disp.html',no=x1,ev=l2,index=indexing,max=no2,tot=no2,list1=val)
		
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

		tuple(x2)
		cur.close()
		l1=['All']
	return render_template('disp.html',no=no2,ev=x2,index=indexing,max=no2,tot=no2,list1=l1)


#page to register for events
@app.route('/reg/<e__name>',methods=['GET','POST'])

def reg(e__name):
	if 'email' not in session :
		return redirect(url_for('index2'))
	if session['eh'] == 'Y' :
		return render_template('error.html')
	cur2=mysql.connection.cursor()
	chek = cur2.execute("SELECT * from events where ename=%s and seats>0",(e__name,))
	if chek == 0:
		return render_template('error.html')
	cur2.execute("SELECT * from details where email=%s",(session['email'],))
	dets = cur2.fetchall()
	cur2.execute("SELECT * from reg where ename=%s and usn=%s",(e__name,dets[0][2]))
	temp=cur2.fetchall()
	cur2.close()
	if temp :
		flash("You've already registered for this event")
		return redirect(url_for('sevents'))
	

	if request.method=='POST' :
		events1=request.form
		sname=dets[0][0]
		usn=dets[0][2]
		email=dets[0][1]
		mem=events1['member']
		ph=dets[0][3]
		cur=mysql.connection.cursor()
		eve_name = e__name
		cur.execute("SELECT * from reg where ename=%s and usn=%s",(eve_name,usn))
		temp=cur.fetchall()
		if temp :
			flash("You've already registered for this event")
			return redirect(url_for('sevents'))
		else :

			cur.execute("INSERT into reg values(%s,%s,%s,%s,%s,%s)",(eve_name,sname,usn,email,ph,mem))
			mysql.connection.commit()
			flash("Registration for the event was successful")
			return redirect(url_for('sevents'))
		cur.close()

		

	return render_template('reg.html',e_name=e__name,details=dets)

#method to unregister from events
@app.route('/unreg/<e__name>',methods=['GET','POST'])

def unreg(e__name):
	cur=mysql.connection.cursor()
	cur.execute("call unregister(%s,%s)",(e__name,session['email'],))
	mysql.connection.commit()
	cur.close()
	flash("Unregistered from the event")
	return redirect(url_for('sevents'))


#home page for event handlers with the option of creating events
@app.route('/homee',methods=['GET','POST'])

def homee():
	if 'email' not in session or 'eh' not in session or session['eh']=='N' :
		return redirect(url_for('index2'))
	else :
		return render_template('homee.html')


#events registered for by a student
@app.route('/sevents',methods=['GET','POST'])

def sevents():
	if 'email' not in session :
		return redirect(url_for('index2'))
	elif session['eh'] == 'N' :
		em=session['email']
		cur=mysql.connection.cursor()
		cur.execute("SELECT e.cname,r.ename,e.edescp,e.dt,e.big_event from reg r,events e where r.ename=e.ename and r.email=%s ORDER BY e.dt",(em,))
		par=cur.fetchall()
		cur.execute("SELECT e.cname,r.ename,e.edescp,e.dt,e.big_event from reg r,pevents e where r.ename=e.ename and r.email=%s ORDER BY e.dt DESC",(em,))
		par2=cur.fetchall()
		cur.execute("SELECT event_num(%s)",(session['email'],))
		eve_num=cur.fetchall()
		cur.close()
		return render_template('sevents.html',ev=par,ev2=par2,num_e=eve_num)
	else :
		return redirect(url_for('settings'))

#creating an event page
@app.route('/create',methods=['GET','POST'])
def create():
	if 'email' not in session or 'eh' not in session or session['eh']=='N' :
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
			cur.execute("SELECT name from login where email=%s",(session['email'],))
			n2=cur.fetchone()
			cur.execute("INSERT INTO events(cname,ename,edescp,seats,dt,tm,venue,big_event) values(%s,%s,%s,%s,%s,%s,%s,%s)",(n2[0],name,desc,seats,dt,tm,venn,op))
			mysql.connection.commit()
			cur.close()
			send_mail(n2[0],name)
			flash("Event was successfully created")
			return redirect(url_for('events'))

		return render_template('create.html')

@app.route('/red_prof')
def red_prof() :
	if session['eh']=='N' :
		return redirect(url_for('sevents'))
	return redirect(url_for('homee'))

@app.route('/test')
def test():
	clubname="Onyx"
	cur=mysql.connection.cursor()
	cur.execute("SELECT email from notify where cname=%s",(clubname,))
	recps=cur.fetchall()
	l1=[]
	for val in recps :
		l1.append(val[0])
	cur.close()
	return render_template('sample.html',lists=l1)


def send_mail(clubname,eventname):
	cur=mysql.connection.cursor()
	cur.execute("SELECT email from notify where cname=%s",(clubname,))
	recps=cur.fetchall()
	l1=[]
	for val in recps :
		l1.append(val[0])
	msg = Message('Event Notification', sender = 'acs.nie1234@gmail.com', recipients = l1)
	msg.body = ("Hello, this is to notify you that "+ clubname + " has a recently added upcoming event titled: "+ eventname +". Please do check it out.")
	mail.send(msg)
	cur.close()

@app.route('/edit',methods=['GET','POST'])
def edit():
	if 'email' not in session :
		return redirect(url_for('index2'))
	cur2=mysql.connection.cursor()
	cur2.execute("SELECT * from details where email=%s",(session['email'],))
	dets = cur2.fetchall()
	cur2.close()	
	if request.method== 'POST' :
		events1=request.form
		sname=events1['name']
		usn=events1['usn']
		email1=events1['email']
		ph=events1['pno']
		cur=mysql.connection.cursor()
		if email1!=session['email'] :  
			c1=cur.execute("SELECT * from login where email=%s",(email1,))
			c2=cur.execute("SELECT * from login where usn=%s",(usn,))
			if c1 or c2 :
				flash("Updates weren't saved as they already exist")
				return redirect(url_for('sevents'))
		cur.execute("UPDATE reg set sname=%s,usn=%s,ph=%s where email=%s",(sname,usn,ph,session['email']))
		cur.execute("UPDATE login set name=%s,email=%s,usn=%s,pno=%s where email=%s ",(sname,email1,usn,ph,session['email'],))
		session['email']=email1
		mysql.connection.commit()
		flash("Updates were saved successfully")
		return redirect(url_for('sevents'))
	return render_template('edit.html',details=dets)

@app.route('/editp',methods=['GET','POST'])
def editp():
	if 'email' not in session :
		return redirect(url_for('index2'))

	if request.method == 'POST' :
		cur=mysql.connection.cursor()
		cur.execute("SELECT passwd from login where email=%s",(session['email'],))
		passw=cur.fetchall()
		dets=request.form
		if dets['opass'] != passw[0][0] :
			return render_template('editp.html',error1='Wrong Password')
		elif dets['pass1'] != dets['pass2'] :
			return render_template('editp.html',error2='Passwords don\'t match')
		elif dets['pass1'] == dets['opass'] :
			return render_template('editp.html',error2='Same as the previous password')
		else :
			cur.execute("UPDATE login set passwd=%s where email=%s",(dets['pass1'],session['email'],))
			mysql.connection.commit()
			cur.close()
			flash("Password was successfully changed")
			return redirect(url_for('sevents'))
	return render_template('editp.html')

@app.route('/settings',methods=['GET','POST'])
def settings():
	if 'email' not in session :
		return redirect(url_for('index2'))
	return render_template('settings.html')

if __name__=='__main__':

	app.run(debug=True)


