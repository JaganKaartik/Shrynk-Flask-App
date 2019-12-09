from shrynk import app, db, bcrypt
from flask import render_template, flash, redirect, url_for
from shrynk.forms import RegistrationForm, LoginForm, URLForm
from flask_login import login_user, current_user, logout_user, login_required
from shrynk.models import User, Dashboard
from datetime import datetime,timedelta
from shrynk.services.urlshorten import urlshorten,urldecode

"""
    Sys for Testing purposes
"""
import sys

"""
    First page that loads when application is started.
"""

@app.route("/")
@app.route("/home",methods=['GET','POST'])
def home():
    print("Logging message on home", flush=True)
    form = URLForm()
    # if form.validate_on_submit():
    genURL = urlshorten(form.longURL.data)
    print(form.longURL.data, flush=True)
    expiry = datetime.now() + timedelta(days=30) 
    mymap = Dashboard(user_id =  form.userid.data,longURL = form.longURL.data,shortURL=genURL,expiry = expiry)
    db.session.add(mymap)
    db.session.commit()
    # else:
    #     flash('Error!','danger')
    return render_template('home.html',form=form)

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route("/login", methods=['GET','POST'])
def loginUser():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form = form)


@app.route("/register", methods=['GET', 'POST'])
def registerUser():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password) 
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success!')
        return redirect(url_for('loginUser'))
    return render_template('register.html', title='Register', form = form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))