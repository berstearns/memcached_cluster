import json
import os
from flask import Flask, session, redirect, render_template, abort
from flask_wtf import FlaskForm, CSRFProtect
from flask_bootstrap import Bootstrap5
from flask_session import Session
from flask_login import LoginManager, login_user, logout_user,\
                         login_required, current_user,\
                            UserMixin
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from pymemcache.client.hash import HashClient

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    submit = SubmitField('Submit')

class User(UserMixin):
    def __init__(self, username, email): 
        self.id = email
        self.username = username

users = {
        "berstearns@gmail.com": User("bernardo1","berstearns@gmail.com")
}

servers = [ tuple(v.split(":")) for v in os.environ.get('MEMCACHED_SERVERS', None).split(',')]

# Create a HashClient to distribute keys across the servers
client = HashClient(servers)

app = Flask(__name__, template_folder="./templates")
app.config['SECRET_KEY']="ac76e1f17e25002a23fea4a5b81bff6885fcf76f1f170e0d04d5d7b96a8089dd"
'''
app.config['OAUTH2_PROVIDERS']={
    "google": {
        'name': "google",
        'client_id': dotenv_config["client_id"],
        'client_secret': dotenv_config["client_secret"],
        'provider_authorization_endpoint': "https://accounts.google.com/o/oauth2/v2/auth",
        'provider_token_endpoint': "https://oauth2.googleapis.com/token",
        'userinfo':{
            "endpoint": "https://openidconnect.googleapis.com/v1/userinfo"
            },
        'scopes': ["openid", "email", "profile"]
    }
}
'''
app.config['PERMANENT_SESSION_LIFETIME']=90
app.config['SESSION_TYPE']="memcached"

app.config['SESSION_MEMCACHED']= client
app.config['SESSION_SERIALIZATION_FORMAT']='json'
bootstrap = Bootstrap5(app)
login_manager = LoginManager()
login_manager.login_view="/login"
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(id):
    print(id)
    return users.get(id)

Session(app)
#csrf = CSRFProtect(app)
'''
("<form action='' method='post'>"
                "<input type='text' id='username' name='username'>"
                "<input type='submit' value='Submit'>"
                "</form>")
'''
@app.route("/login",methods=["GET"])
def index():
    if session.get("user", False):
        return redirect("/homepage")
    else:
        formTemplate=LoginForm()
        return render_template("login.jinja2",
                               form=formTemplate
                               ) 

@app.route("/login",methods=["POST"])
def login_submit():
    form = LoginForm()
    next_ = redirect("/login")
    if form.validate_on_submit():
        '''session['user'] = {
                "username": form.username.data
                }'''
        user_search = users.get(form.email.data, None)
        print(user_search)
        if user_search is not None:
            #user.username = form.username.data
            #user = UserMixin()
            user = user_search
            login_user(user)
            next_ = redirect("/homepage") 
    return next_

@app.route("/logout",methods=["GET"])
def logout_submit():
    next_ = redirect("/login") 
    logout_user()
    return next_

@app.route("/homepage")
@login_required
def home():
    return render_template("homepage.jinja2",
                           current_user=current_user
                           ) 


@app.route('/set', methods=['POST'])
def set_key():
    key = request.form.get('key')
    value = request.form.get('value')
    server = client.hasher.get_node(key)
    client.set(key, value)
    return f"Key '{key}' set to '{value}' stored in {server}."

@app.route('/get', methods=['GET'])
def get_key():
    key = request.args.get('key')
    value = client.get(key)
    server = client.hasher.get_node(key)
    return f"Value for '{key}': {value.decode('utf-8') if value else 'None'} from server {server}"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def get_dir(path):
    return redirect("/login")


if __name__ == "__main__":
    import sys
    # port=int(sys.argv[1])
    app.run(host="0.0.0.0", port=80,debug=True)

