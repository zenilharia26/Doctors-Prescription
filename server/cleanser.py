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

if __name__ == '__main__':
    app.run(debug=True)
    