from flask import Blueprint
blueuser=Blueprint('user',__name__)   #蓝图的对象的名称=Blueprint('自定义蓝图名称',__name__) 

from flask import request, jsonify

from flask_login import LoginManager
from flask_login import UserMixin, login_user, logout_user, login_required, current_user

from sqlalchemy import and_, false, or_, true
from app import db,app

from models import Userinfo


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Access denied.'
login_manager.init_app(app)

class User(UserMixin):
    pass

# class Userinfo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     password = db.Column(db.String(256), unique=False)
#     email = db.Column(db.String(120), unique=True)

#     def __repr__(self):
#         return '<User %r>' % self.username

@login_manager.user_loader
def load_user(username):
    if query_user(username) is not None:
        curr_user = User()
        curr_user.id = username

        return curr_user

def query_user(username):
    user = Userinfo.query.filter(Userinfo.username == username).first()
    if user is None:
        return False
    else:
        return True

def valid_login(username, password):
    user = Userinfo.query.filter(and_(Userinfo.username == username, Userinfo.password == password)).first()
    if user:
        return True
    else:
        return False

# 注册检验（用户名、邮箱验证）
def valid_regist(username, email):
    user = Userinfo.query.filter(or_(Userinfo.username == username, Userinfo.email == email)).first()
    if user:
        return False
    else:
        return True

@blueuser.route('/bluetest')
def bluetest():
    return 'bluetest'

# 4.注册
@blueuser.route('/regist', methods=['GET','POST'])
def regist():
    error = None
    data = {
        'status': False,
        'error': None,
    }
    if request.method == 'POST':
        data_input = request.get_json()
        print("==============================")
        print(data_input)
        if data_input['password1'] != data_input['password2']:
            error = '两次密码不相同！'
        elif valid_regist(data_input['username'], data_input['email']):
            print("==============================")
            print(data_input)
            user = Userinfo(username=data_input['username'], password=data_input['password1'], email=data_input['email'])
            db.session.add(user)
            db.session.commit()
            data['status']=True
        else:
            error = '该用户名或邮箱已被注册！'
            data['error']=error
    return jsonify(data)


@blueuser.route('/login', methods=['GET', 'POST'])
def login():
    data = {
        'status': False,
        'error': None
    }
    if request.method == 'POST':
        data_input = request.get_json()
        username = data_input['username']
        password = data_input['password']

        if valid_login(username,password):
            curr_user = User()
            curr_user.id = username

            login_user(curr_user)
            data['status']=True,
        else:
            data['error']= "Wrong username or password!"

    return jsonify(data)

@blueuser.route('/login_status', methods=['GET'])
def login_status():
    data = {
        'status': False,
    }
    print(current_user)
    if current_user.is_authenticated:
        data['status']=True
        data['username']=current_user.id
    return jsonify(data)


@blueuser.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'data':'Logged out successfully!'})

# @blueuser.route('/clear_session', methods=['GET', 'POST'])
# def clean_session():
#     session.clear()
#     print("session")
#     print(session)
#     return jsonify({})

# # 5.个人中心
# @app.route('/panel')
# @login_required
# def panel():
#     username = session.get('username')
#     user = User.query.filter(User.username == username).first()
#     return render_template("panel.html", user=user)