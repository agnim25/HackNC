from flask import Flask, render_template, request, url_for, redirect, session
from forms import *
from model import generate_recommendations
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/', methods=["GET", "POST"])
def landing():
    title = 'Intellistocks'
    form = AuthForm()
    form_name = 'Auth'
    if request.method == 'POST':
        session['name'] = request.form.get("name", None)
        session['email'] = request.form.get("email", None)
        session['new'] = request.form.get("new", None)
        if not (session['name'] is None):
            return redirect(url_for('dashboard'))
    return render_template('landing.html', title = title, form = form, form_name = form_name)

@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    if not 'name' in session or ('name' in session and session['name'] is None):
        return redirect(url_for('landing'))
    if session['new'] == 'true':
        title = 'Welcome, ' + str(session['name']).split(' ')[0]
    else:
        title = 'Welcome back, ' + str(session['name']).split(' ')[0]
    form = PredictForm()
    form_name = 'Predict Daily Market Change Based on News Headlines'
    if request.method == 'POST':
        text = request.form.get("text")
        return redirect(url_for('results', text=text))
    return render_template('dashboard.html', title=title, form=form, form_name=form_name, email=session['email'])

@app.route('/results', methods=["GET", "POST"])
def results():
    if not 'name' in session or ('name' in session and session['name'] is None):
        return redirect(url_for('landing'))
    title = 'Market Change Prediction Results'
    text = str(request.args.get("text"))
    recs = generate_recommendations(text)
    form = ReturnForm()
    form_name = 'Return to Dashboard'
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    return render_template('results.html', title=title, form=form, form_name=form_name, text=text, recs=recs)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
