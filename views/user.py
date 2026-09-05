from flask import Blueprint
blueuser=Blueprint('user',__name__)   #蓝图的对象的名称=Blueprint('自定义蓝图名称',__name__) 

from flask import request, jsonify

from flask_login import LoginManager
from flask_login import UserMixin, login_user, logout_user, login_required, current_user

from sqlalchemy import and_, false, or_, true
from models import Userinfo, db
from werkzeug.security import check_password_hash, generate_password_hash


login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Access denied.'
class User(UserMixin):
    pass

@login_manager.unauthorized_handler
def unauth_handler():
    return jsonify({'status': False, 'error': 'Access denied.'}), 401

@login_manager.user_loader
def load_user(username):
    if query_user(username):
        curr_user = User()
        curr_user.id = username

        return curr_user
    return None

def query_user(username):
    user = Userinfo.query.filter(Userinfo.username == username).first()
    if user is None:
        return False
    else:
        return True

def valid_login(username, password):
    user = Userinfo.query.filter(Userinfo.username == username).first()
    if user is None:
        return False

    password_is_hashed = user.password.startswith(('pbkdf2:', 'scrypt:'))
    if password_is_hashed:
        return check_password_hash(user.password, password)

    # Keep old databases usable and upgrade a legacy plaintext password after
    # the first successful login.
    if user.password == password:
        user.password = generate_password_hash(password)
        db.session.commit()
        return True
    return False

def valid_input_regist(username,password1,password2,email):
    data = {
        'status': False,
        'error': None,
    }
    data['error']="目前未开放注册"
    return data
    if username is None:
        data['error']="未输入用户名"
        return data
    if password1 is None:
        data['error']="未输入密码"
        return data
    if password2 is None:
        data['error']="没有确认密码"
        return data
    if email is None:
        data['error']="未输入邮箱"
        return data
    if len(password1)<6:
        data['error']="密码需要至少有6位"
        return data
    if password1!=password2:
        data['error']="两次输入密码不相同"
        return data
    # 经过以上验证之后，认为数据合法
    data['status']=True
    return data

def valid_input_login(username,password):
    data = {
        'status': False,
        'error': None,
    }
    if username is None:
        data['error']="未输入用户名"
        return data
    if password is None:
        data['error']="未输入密码"
        return data
    if len(password)<6:
        data['error']="密码需要至少有6位"
        return data
    if len(password)>16:
        data['error']="密码不能多于16位"
        return data
    # 经过以上验证之后，认为数据合法
    data['status']=True
    return data

# 注册检验（用户名、邮箱验证）
def valid_regist(username, email):
    user = Userinfo.query.filter(or_(Userinfo.username == username, Userinfo.email == email)).first()
    if user:
        return False
    else:
        return True

# 4.注册
@blueuser.route('/regist', methods=['GET','POST'])
def regist():
    error = None
    data = {
        'status': False,
        'error': None,
    }
    if request.method == 'POST':
        data_input = request.get_json(silent=True) or {}
        username = data_input.get('username')
        password1=data_input.get('password1')
        password2=data_input.get('password2')
        email=data_input.get('email')
        data = valid_input_regist(username,password1,password2,email)
        if data['status']:
            if valid_regist(data_input['username'], data_input['email']):
                user = Userinfo(
                    username=data_input['username'],
                    password=generate_password_hash(data_input['password1']),
                    email=data_input['email'],
                    submitted=0,
                    correct=0,
                )
                db.session.add(user)
                db.session.commit()
                data['status']=True
            else:
                error = '该用户名或邮箱已被注册！'
                data['status']=False
                data['error']=error
    print(data)
    return jsonify(data)


@blueuser.route('/login', methods=['GET', 'POST'])
def login():
    data = {
        'status': False,
        'error': None
    }
    if request.method == 'POST':
        data_input = request.get_json(silent=True) or {}
        username = data_input.get('username')
        password = data_input.get('password')

        data = valid_input_login(username,password)

        # 验证输入格式是否合法
        if data['status']:
            # 在数据库里查找
            if valid_login(username,password):
                curr_user = User()
                curr_user.id = username
                login_user(curr_user)
            else:
                data['status']=False
                data['error']= "用户名或密码错误"

    print(data)
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
