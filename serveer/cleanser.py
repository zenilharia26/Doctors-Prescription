from flask import Flask
app = Flask(__name__)


@app.route('/name')
def nameresolver():
    return "Hello World!"

@app.route('/age')
def ageresolvere():
    return "Heloo world"

@app.route('/medicines')
def medicinesresolverr():
    return "dont be high"

@app.route('/advice')
def adviceresolver():
    return "be down to earth"

@app.route('/number')
def phone():
    return 'bla bla'

    

if __name__ == '__main__':
    app.run()