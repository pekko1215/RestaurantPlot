#/usr/bin/python3.5

import urllib.parse
import json,base64
from flask import Flask,render_template,request,redirect,session,url_for,jsonify,Blueprint
import util
from db import Restraurant,DBSession,User
from API import APIRouter

app = Flask(__name__)
app.config.from_pyfile('./config.cfg')

app.config['SESSION_STATE'] = util.randomname(8)
print(APIRouter)
app.register_blueprint(APIRouter,url_prefix='/api')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/application')
@util.login_required
def application():
    return render_template('application.html')


@app.route('/login')
def login():
    if 'name' in session:
        return redirect(url_for('application'))
    return redirect('https://accounts.google.com/o/oauth2/auth?{}'.format(urllib.parse.urlencode({
        'client_id':app.config['CLIENT_ID'],
        'scope':'profile',
        'redirect_uri':app.config['REDICET_URL'],
        'state':app.config['SESSION_STATE'],
        'openid.realm':app.config['REALM'],
        'response_type':'code'
    })))

@app.route('/redirect')
def oauth_redirect():
    print(session)
    if request.args.get('state') != app.config['SESSION_STATE']:
        return 'Invalid state'
    data = urllib.request.urlopen('https://www.googleapis.com/oauth2/v4/token',urllib.parse.urlencode({
        'code': request.args.get('code'),
		'client_id': app.config['CLIENT_ID'],
		'client_secret': app.config['CLIENT_SECRET'],
        'redirect_uri':app.config['REDICET_URL'],
		'grant_type': 'authorization_code'
    }).encode('utf8')).read()
    data = json.loads(data.decode('utf8'))

    id_token = data['id_token'].split('.')[1]
    id_token = id_token + '=' * (4 - len(id_token)%4)  # パディングが足りなかったりするっぽいので補う
    id_token = base64.b64decode(id_token,'-_')
    id_token = json.loads(id_token.decode('utf8'))
    session['user_id'] = id_token['sub']
    
    users = DBSession.query(User)\
        .filter(User.id == id_token['sub'])\
        .all()
    print(session)
    print(users)
    if len(users) != 0:
        session['name'] = users[0].name
        return redirect(url_for('application'))

    return redirect(url_for('register'))

@app.route('/register',methods=["GET"])
def register():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/register',methods=["POST"])
def post_register():
    if 'user_id' not in session or \
    'name' not in request.form:
        return 'Invalied Data'
    name = request.form['name']
    id = session['user_id']
    
    user = User()
    user.id = id
    user.name = name

    DBSession.add(user)
    DBSession.commit()

    session['name'] = name
    return redirect(url_for('application'))

@app.route('/logout')
def logout():
    session.pop('user_id',None)
    session.pop('name',None)
    return redirect(url_for('index'))

app.secret_key = 'hogehogenekonekonya-n'

app.run(host='localhost',port=25050)
