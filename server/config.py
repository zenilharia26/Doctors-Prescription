from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:1234@localhost/doctordesc'
db=SQLAlchemy(app)

class docregister(db.Model):
	user_id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(100),unique=True)
	email=db.Column(db.String(100),unique=True)
	password=db.Column(db.String(100),unique=True)
	contact=db.Column(db.String(100),unique=True)

	def __init__(self,name,email,password,contact):
		self.name=name
		self.email=email
		self.password=password
		self.contact=contact
	def __ret__(self):
	    return '<User %r>' % self.username	 
@app.route('/')
def index():
	return render_template("register.html")
@app.route('/register',methods=['POST'])
def adding():
	if request.method=='POST':
	     user=docregister(request.form.get('namy'),request.form.get('email'),request.form.get('password'),request.form.get('contact'))
	     print(request.form)	
	     db.session.add(user)	
	     db.session.commit()
	     return(redirect(url_for("loginuser")))
@app.route('/login')
def loginuser():
	return render_template('login.html')	     




if __name__=="__main__":
    app.run(debug=True);