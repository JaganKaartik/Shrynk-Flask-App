from shrynk import app, db, bcrypt
from flask import render_template, flash, redirect, url_for
from shrynk.forms import RegistrationForm, LoginForm, URLForm
from flask_login import login_user, current_user, logout_user, login_required
from shrynk.models import User, Dashboard
from datetime import datetime,timedelta
from flask_admin.contrib.sqla import ModelView
from shrynk.services.urlshorten import urlshorten
from shrynk.services.randomString import generateRandomString
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
    flash('Login Successful', 'success')
    print("Logging message on home", flush=True)
    form = URLForm()
    # if form.validate_on_submit():
    if form.validate_on_submit():
        print("Logging message on submit", flush=True)
        genURL = urlshorten(form.longURL.data)
        # Implementing Check for Re-dundant URLs
        # Testing
        # genURL = "http://127.0.0.1:5000/"+genURL
        # Deployment
        genURL = "http://shrynk.herokuapp.com/"+genURL
        urls =  Dashboard.query.all()
        for i in urls:
            if i.shortURL==genURL:
                print("Re-dundant URL",flush = True)
                res = generateRandomString()
                genURL = urlshorten(form.longURL.data+res)
                # Testing
                # genURL = "http://127.0.0.1:5000/"+genURL
                # Deployment
                genURL = "http://shrynk.herokuapp.com/"+genURL
        # End of Check for Re-dundant URLs
        expiry = datetime.now() + timedelta(days=30) 
        mymap = Dashboard(user_id =  form.userid.data,longURL = form.longURL.data,shortURL=genURL,expiry = expiry)
        db.session.add(mymap)
        db.session.commit()
    else:
        flash(f'Error!','danger')
    result = []
    if current_user.is_authenticated:
        result =  Dashboard.query.filter_by(user_id=current_user.id).all()
    return render_template('home.html',form=form,data=result)

@app.route('/<shorturl>')
def linker(shorturl):
    shorturl = "http://127.0.0.1:5000/" + shorturl
    url =  Dashboard.query.filter_by(shortURL=shorturl).first()
    return redirect(url.longURL,code=302)

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


class MyModelView(ModelView):
    def is_accessible(self):
        if User.query.filter(current_user.username == 'Admin').first():
            return True
        else:
            return False

            def inaccessible_callback(self,name,**kwargs):
                return redirect(url_for('login'))
