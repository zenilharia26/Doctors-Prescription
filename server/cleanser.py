from flask import Flask,render_template,request,redirect,url_for,session,flash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
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
class patient(db.Model):
    patient_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    symptoms=db.Column(db.String(1000))
    diagnosis=db.Column(db.String(1000))
    prescription=db.Column(db.String(2000))
    docpres=db.Column(db.String(100))
    def __init__(self,name,symptoms,diagnosis,prescription,docpres):
        self.name=name
        self.symptoms=symptoms
        self.diagnosis=diagnosis
        self.prescription=prescription
        self.docpres=docpres
        
   
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

stop = stopwords.words('english')
tags = ['name']
string = "Zenil Haria"

def extract_phone_numbers(data):
    data = data.replace(' ','')
    return data

def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)

def ie_preprocess(document):
    sentences = sent_tokenize(document)
    return sentences

def extract_names(document):
    names = []
    sentences = ie_preprocess(document)
    for word in sentences:
        word_list = nltk.word_tokenize(word)
        word_list = [w for w in word_list if not w in stop]  
        tagged = nltk.pos_tag(word_list)
        for tag in tagged:
            if tag[1] in ['NNS', 'NNP', 'NN'] and tag[0] not in tags:
                names.append(tag[0])
    print(names)
    data = ''
    for word in names:
        data += word + ' '
    return data


@app.route('/extract', methods=['POST'])
def extract():
    default_msg = 'Name nai aya'
    if request.method == 'POST':
        keyword= request.form['type']
        data = request.form['data']
        print(keyword)
        print(data)
        if keyword == 'name':
            result = extract_names(data)
        elif keyword == 'phone':
            result = extract_phone_numbers(data)
        elif keyword == 'email':
            result = extract_email_addresses(data)
        else:
            result = 'Gand mara'
        print(result)
        return result
    return default_msg

@app.route('/email')
def emailresolver():
    emails = extract_email_addresses(string)
    return emails[0]
    
@app.route('/tryreq')
def trial():
    return render_template('try.html')

@app.route('/recorder')
def record():
    return render_template('js.html')



@app.route('/newuser')
def index():
    if 'name' in session:
        return render_template("search.html",name=session['name'])
    else:
        return render_template("register.html")

@app.route('/')
def dashboard():
    return render_template('register.html')

@app.route('/register',methods=['POST'])
def adding():
    if request.method=='POST':
         
         user=docregister(request.form.get('name'),request.form.get('email'),request.form.get('password'),request.form.get('contact'))
         print(request.form)    
         db.session.add(user)   
         db.session.commit()
         return(redirect(url_for("loginuser")))

@app.route('/login')
def loginuser():
    if session:
        return render_template("search.html",name=session['name'])
    else:
        return render_template("login.html")        

@app.route('/validate',methods=['POST'])
def validation():
        if request.method=='POST':
            emails=request.form.get('email')
            passwords=request.form.get('password')
            user=docregister.query.filter_by(email=emails).first()
            if user:
                if user.password==passwords:
                    session['name']=user.name
                    print(session['name'])  
                    return render_template('search.html',name=session['name'])
            flash("username or password not found","danger")
            return (redirect(url_for('loginuser')))        
             
@app.route('/logout')
def logout():
        if 'name' in session:
            session.pop('name',None)
            return render_template('register.html')

@app.route('/record')
def speech():
    if 'name' in session:
        return render_template('speech.html',name=session['name'])
    else:
       return (redirect(url_for('loginuser')))     
@app.route('/addpatient',methods=['POST'])
def addpatients():
    if  session:
        if request.method=='POST':
             user1=patient(request.form.get('name'),request.form.get('symptoms'),request.form.get('diagnosis'),request.form.get('prescription'),session['name'])
             print(request.form.get('symptoms'))
             print(session['name'])
             print(request.form.get('diagnosis'))
             db.session.add(user1)   
             db.session.commit() 
             return(redirect(url_for("speech")))
    else:
       return (redirect(url_for('loginuser')))
@app.route('/search',methods=['POST'])
def search():
    if request.method=='POST':

        ser=form.request.get('search')
        find=patients.query.filter(patients.name.ilike(ser)).all()
        for row in find:
            print(row)

if __name__ == '__main__':
    app.debug = True
    app.secret_key="384tyhhfhr"
    app.run()
    
    