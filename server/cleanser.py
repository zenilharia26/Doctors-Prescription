from flask import Flask,render_template,request,redirect,url_for,session,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from virtru_tdf3_python import Client,Policy,EncryptFileParam,Protocol
import yagmail
import os

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
        elif keyword in ('prescription','diagnosis','advice','symptoms'):
            result=data    
        else:
            result = ''
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
         pw_hash = generate_password_hash(request.form.get('password'))
         user=docregister(request.form.get('name'),request.form.get('email'),pw_hash,request.form.get('contact'))
            
         db.session.add(user)   
         db.session.commit()
         return(redirect(url_for("loginuser")))

@app.route('/login')
def loginuser():
    if 'name' in session:
        return render_template("search.html",name=session['name'])
    else:
        return render_template("register.html") 


@app.route('/validate',methods=['POST'])
def validation():
        if request.method=='POST':
            emails=request.form.get('email')
            passwords=request.form.get('password')
            user=docregister.query.filter_by(email=emails).first()
            if user:
                if check_password_hash(user.password, passwords):
                    session['name']=user.name
                    
                    return render_template('search.html',name=session['name'])
            errors="username or password not found"
            return render_template('register.html',error=errors) 


             
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
    if  'name' in session:
        if request.method=='POST':
             user1=patient(request.form.get('name'),request.form.get('symptoms'),request.form.get('diagnosis'),request.form.get('prescription'),session['name'])
             print(request.form.get('symptoms'))
             
             print(request.form.get('diagnosis'))
             db.session.add(user1)   
             db.session.commit() 
             return(redirect(url_for("speech")))
    else:
       return (redirect(url_for('loginuser')))
@app.route('/search',methods=['POST'])
def search():
    if request.method=='POST':

        ser=request.form.get('search')
        find=patient.query.filter(patient.name.contains(ser)).filter(patient.docpres==session['name']).all()
        return render_template('find.html',row=find)

    return render_template('search.html',name=session['name'])      
@app.route('/pdf',methods=['POST'])
def getpdf():
    if request.method=='POST':
        print(request.files)
        latestfile=request.files['data']
        latestfile.save(os.path.join(app.root_path,'static','bg.pdf'))
        client = Client(owner = "vatsal.palan@somaiya.edu",
                app_id = "a484aecf-af64-4538-a69f-06543b5996b4")
        policy = Policy()
        policy.share_with_users(["aditya.sehgal@somaiya.edu",'zenil.haria@somaiya.edu','mankadarnav@gmail.com'])
        client.set_protocol(Protocol.Zip)
        param = EncryptFileParam(in_file_path=os.path.join(app.root_path, 'static', 'bg.pdf'),
                         out_file_path=os.path.join(app.root_path, 'static',  'bg.pdf.tdf3'))
        param.set_policy(policy)
        client.encrypt_file(encrypt_file_param=param)
        
        yag = yagmail.SMTP("vatsal.palan@somaiya.edu", "Vats@506")
        pathy= str(os.path.join(app.root_path, 'static',  'bg.pdf.tdf3'))
        contents = [pathy,'To decrypt the file visit the provided url','https://demos.developer.virtru.com/dd/index.html '
            
        ]
        yag.send("aditya.sehgal@somaiya.edu", "Test Email", contents)
        yag.send("zenil.haria@somaiya.edu", "Test Email", contents)
        yag.send("mankadarnav@gmail.com", "Test Email", contents)

        return 'hi'
    return 'hi'      

if __name__ == '__main__':
    app.debug = True
    app.secret_key="384tyhhfhr"
    app.run()
    
    