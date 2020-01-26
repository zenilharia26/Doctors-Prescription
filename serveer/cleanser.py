from flask import Flask
app = Flask(__name__)

import re
import nltk
from nltk.corpus import stopwords
"""nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')"""

stop = stopwords.words('english')

string = """
abcd123@gmail.com

"""

def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', number) for number in phone_numbers]

def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)

def ie_preprocess(document):
    document = ' '.join([i for i in document.split() if i not in stop])
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

def extract_names(document):
    names = []
    sentences = ie_preprocess(document)
    print(sentences)
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            print(chunk)
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    names.append(' '.join([c[0] for c in chunk]))
    return names


@app.route('/name')
def nameresolver():
    names = extract_names(string)
    return "Hello World!"

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
    