from flask import Flask
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
string = "My name is Zenil Rajesh Haria"

def extract_phone_numbers(string):
    r = re.compile(r'(\d{10})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', number) for number in phone_numbers]

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
    return names[0]


@app.route('/name')
def nameresolver():
    names = extract_names(string)
    print(names)
    return names

@app.route('/age')
def ageresolver():
    return "Heloo world"

@app.route('/medicines')
def medicinesresolver():
    return "dont be high"

@app.route('/advice')
def adviceresolver():
    return "be down to earth"

@app.route('/number')
def phoneresolver():
    numbers = extract_phone_numbers(string)
    return numbers[0]

@app.route('/email')
def emailresolver():
    emails = extract_email_addresses(string)
    return emails[0]
    

if __name__ == '__main__':
    app.debug = True
    app.run()
    