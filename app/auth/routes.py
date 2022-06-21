from flask import Blueprint, render_template,request,redirect,url_for,flash
from app.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user,login_required,logout_user


auth = Blueprint('auth',__name__,template_folder='auth_templates',url_prefix='/auth',static_folder='auth_static')
from .authforms import LoginForm, RegistrationForm

#create our first route within the blueprint
@auth.route('/login', methods=['GET','POST'])
def login():
    lform = LoginForm()
    if request.method =='POST':
   
        if lform.validate_on_submit():
            user=User.query.filter_by(username=lform.username.data).first()
            print(user)
            if user and check_password_hash(user.password, lform.password.data):
                login_user(user)
                flash(f'Successful Login for user {user.username}!',category='success')
            else:
                flash('Username and password must match!','danger')
            return redirect((url_for('home')))
        flash('Incorrect username or password, please try again.','danger')
        return redirect(url_for('auth.login'))
    return render_template('signin.html',form=lform)



@auth.route('/register', methods=['GET', 'POST'])
def register():
    rform = RegistrationForm()
    if request.method == 'POST':
        if rform.validate_on_submit():
            newuser = User(rform.username.data, rform.email.data, rform.password.data, rform.first_name.data, rform.last_name.data)
            try:
                db.session.add(newuser)
                db.session.commit()
            except:
                flash('Username or email already registered! Please try a different one.', category='danger')
                return redirect(url_for('auth.register'))
            login_user(newuser)
            flash(f'Welcome! Thank you for registering, {newuser.username}!', 'info')
            return redirect(url_for('home'))
        else:
            flash('Sorry, passwords do not match. Please try again.', 'danger')
            return redirect(url_for('auth.register'))
    elif request.method == 'GET':
        return render_template('register.html', form=rform)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been signed out','info')
    return redirect(url_for('auth.login'))