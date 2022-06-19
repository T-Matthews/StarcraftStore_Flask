from flask import Blueprint, render_template,request

auth = Blueprint('auth',__name__,template_folder='auth_templates',url_prefix='/auth',static_folder='auth_static')
from .authforms import LoginForm

#create our first route within the blueprint
@auth.route('/login',method=['GET','POST'])
def login():
    lform = LoginForm()
    if request.method =='POST':
        print(lform.data)
        return 'Thanks for logging in.'
    return render_template('signin.html', form=lform)
