from flask import Flask,render_template,request
app = Flask(__name__)

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
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

@app.route('/doctorsignup',methods = ['POST', 'GET'])
@app.route('/doctorlogin',methods = ['POST', 'GET'])
def doctorlogin():
	if "email" in session:
		data=[session["email"],session["password"]]
		return redirect(url_for('index'))
	elif request.method=="POST":
		if 'doctorlogin' in request.form:
			email=request.form['email']
			password=request.form['password']
			cur.execute("SELECT * FROM doctors WHERE email=%s AND password=crypt(%s,password);",(email,password,))
			data=cur.fetchone()
			#cur.close()
			#con.close()
			print(data)
			if data:
				session["fullname"]=data[0]
				session["phoneno"]=data[1]
				session["email"]=data[2]
				session["password"]=data[3]
				session["certificate"]=data[4]
				flash('Logged in successfully! Welcome Dr. '+session["fullname"],'success')
				return redirect(url_for('index'))
			else:
				flash('Invalid username or password. Please try again ','warning')
				return render_template('doctorlogin.html',doctorlogin='active-link')
        
        elif 'doctorsignup' in request.form:
            fullname=request.form['fullname']
            phoneno=request.form['phoneno']
            email=request.form['email']
            password=request.form['password']
            certificate=request.form['certificate']
            print(request.form)
            cur.execute("INSERT INTO doctors(fullname,phoneno,email,password,certificate) VALUES(%s,%s,%s,crypt(%s,gen_salt('bf')),%);",(fullname,phoneno,email,password,certificate,))
            con.commit()
            # cur.execute("INSERT INTO regusers VALUES(%s,0);",(uname,))
            # con.commit()
            #cur.close()
            #con.close()
            flash('Registration successful! Please login to continue','success')
            return render_template('doctorlogin.html',doctorlogin='active-link')
	return render_template('doctorlogin.html',doctorlogin='active-link')

@app.route('/logout',methods = ['POST', 'GET'])
def logout():
    session.pop("fullname")
    session.pop("phoneno")
    session.pop("email")
    session.pop("password")
    session.pop("certificate")
    flash('Logged out successfully','success')
    return redirect(url_for('index'))    

if __name__ == '__main__':
    app.debug = True
    app.run()
    
    