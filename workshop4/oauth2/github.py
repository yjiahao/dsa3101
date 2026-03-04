import os, functools
from dotenv import load_dotenv

from flask import (
    Flask, redirect, url_for, session, g,
    render_template_string
)
from flask_dance.contrib.github import make_github_blueprint, github

load_dotenv()  

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
app.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
github_bp = make_github_blueprint(scope="user")
app.register_blueprint(github_bp, url_prefix="/login")

@app.route("/")
def index(): 
    if not github.authorized: 
        return redirect(url_for("github.login")) 
    resp = github.get("/user") 
    session['user'] = resp.json()["login"]

    return render_template_string(""" 
    <H3> Congratulations, {{ x }} ! </H3>

    <p> You have been successfully authenticated! </p>
    """, x = session['user'])

def login_required(view): 
    @functools.wraps(view) 
    def wrapped_view(**kwargs): 
        if "user" not in session:
            return redirect(url_for('index')) 
        return view(**kwargs) 
    return wrapped_view

@app.route("/myemails")
@login_required
def list_emails():
    resp2 = github.get("/user/emails") 
    return render_template_string("""
    Your email addresses are: 
    <ul>
      {% for ii in  x  %}
        <li>{{ ii['email'] }}</li>
      {% endfor %}
    </ul>

    """, x = resp2.json())

@app.route("/logout")
def logout(): 
    session.clear()
    return "You have successfully logged out."
