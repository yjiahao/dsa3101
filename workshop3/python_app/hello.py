from flask import Flask, request

app = Flask(__name__)

@app.route("/handler")
def hello_world(): 
    lang = request.args.get('value')
    print(f'Hello, World! The value sent to handler is {lang}')

    return f'<emph> Message received is {lang}!</emph>'
