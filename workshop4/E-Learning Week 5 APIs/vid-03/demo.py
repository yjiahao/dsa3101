from flask import Flask, jsonify 
 
app = Flask(__name__) 
  
@app.route('/api') 
def demo_fn(): 
    return jsonify({'Hello': 'World!'})

@app.route('/api/<int:x>') 
def demo_fn2(x): 
    return jsonify({'Hello': 'World!', 'Number': f'{x}'})
