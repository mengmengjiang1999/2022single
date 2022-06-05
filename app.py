from crypt import methods
from enum import unique
from cv2 import Algorithm
from flask import Flask, escape, url_for, request, render_template, jsonify, json, redirect, session,flash

from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, false, or_, true

from flask_login import LoginManager
from flask_login import UserMixin, login_user, logout_user, login_required, current_user

class User(UserMixin):
    pass

import sys
import os
import random

from datetime import datetime
import hashlib

import base64
def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))

def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')

# from flask_sqlalchemy import SQLAlchemy  # 导入扩展类

app = Flask(__name__)

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
 
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

# Import for Migrations
from flask_migrate import Migrate, migrate
 
# Settings for migrations
migrate = Migrate(app, db)

# login

app.secret_key= '23232333'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# login_manager = LoginManager()  # 实例化登录管理对象
# login_manager.init_app(app)  # 初始化应用
# login_manager.login_view = 'login'  # 设置用户登录视图函数 endpoint

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Access denied.'
login_manager.init_app(app)



@login_manager.user_loader
def load_user(username):
    if query_user(username) is not None:
        curr_user = User()
        curr_user.id = username

        return curr_user

from werkzeug.security import generate_password_hash
import uuid

import click

@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column()
    username = db.Column(db.String(80), unique=False)
    problem_id = db.Column(db.String(50), unique=True, nullable=False)
    problem_type = db.Column(db.Integer, unique=False, nullable=False)
    status = db.Column(db.Integer, unique=False, nullable=False)
    # status: 0:还未做，1:做了答案正确，2：做了，答案错误
 
    def __repr__(self):
        return "id : {self.id}, problem_id: {self.problem_id}, status: {self.status}"

class Userinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(256), unique=False)
    email = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return '<User %r>' % self.username

def query_user(username):
    user = Userinfo.query.filter(Userinfo.username == username).first()
    if user is None:
        return False
    else:
        return True

def query_problems(username):
    prblm = Problem.query.filter(Problem.username == username).all()
    return prblm
    # plm = Problem.query.filter(Problem.)

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

# # 登录
# def login_required(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         if session.get('username'):
#             return func(*args, **kwargs)
#         else:
#             # return redirect(url_for('login', next=request.url)) # 
#             return {'error': "error"}
#     return wrapper

# 4.注册
@app.route('/regist', methods=['GET','POST'])
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

@app.route('/login', methods=['GET', 'POST'])
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

@app.route('/login_status', methods=['GET'])
def login_status():
    data = {
        'status': False,
    }
    print(current_user)
    if current_user.is_authenticated:
        data['status']=True
        data['username']=current_user.id
    return jsonify(data)

@app.route('/test', methods=['GET','POST'])
def test():
    print(request.form)
    return "haha"

'''
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     data = {
#         'error': None
#     }
#     error = None
#     if request.method == 'POST':
#         data_input = request.get_json()
#         print(data_input)
#         if valid_login(data_input['username'], data_input['password']):
#             # flash("成功登录！")
#             username = data_input['username']
#             # session['\{\0}'.format(username)] = username
#             session['username']=username
#             print("session")
#             print(session)
#             # return redirect(url_for('index'))
#             print("login success!")
#         else:
#             error = '错误的用户名或密码！'
#             data['error'] = error

#     # return render_template('login.html', error=error)
#     return jsonify(data)

# 3.注销
# @app.route('/logout', methods=['GET', 'POST'])
# @login_required
# def logout():
#     data = {
#         'error': None
#     }
#     if request.method == 'POST':
#         data_input = request.get_json()
#         session.pop('username', None)
#         print("logout_session")
#         print(session)
#         # return redirect(url_for('home'))
#     return jsonify(data)
'''

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'data':'Logged out successfully!'})

@app.route('/clear_session', methods=['GET', 'POST'])
def clean_session():
    session.clear()
    print("session")
    print(session)
    return jsonify({})

# # 5.个人中心
# @app.route('/panel')
# @login_required
# def panel():
#     username = session.get('username')
#     user = User.query.filter(User.username == username).first()
#     return render_template("panel.html", user=user)



@app.route('/algorithm/dijkstra', methods = ['GET', 'POST'])
@login_required
def dijkstra():
    if request.method == 'GET':
        # N = request.form['N']

        # 生成题目和答案
        N = random.randint(5,8)

        from run import run

        filepath_in, filepath_ans, filepath_problem, filepath_image = run()

        # file_in = open(filepath_in,"r")
        # data_in = file_in.read()
        # file_in.close()

        time = datetime.timestamp(datetime.now())
        # print(time)
        data_sha = hashlib.sha256(str(time).encode('utf-8')).hexdigest()  
        print(data_sha) 
        
        # problem_id = data_sha

        # 对数据库的修改
        prblm = Problem(username=current_user.id, problem_id=data_sha, problem_type=0, status = 0)
        db.session.add(prblm)
        db.session.commit()

        # 保存答案
        os.system('cp ' + filepath_problem + ' ./data/problem/' + str(data_sha) + '.problem')
        os.system('cp ' + filepath_ans + ' ./data/answer/' + str(data_sha) + '.ans')
        os.system('cp ' + filepath_image + ' ./data/image/' + str(data_sha) + '.png')

        # file_ans = open(filepath_ans,"r")
        # data_ans = file_ans.read()
        # file_ans.close()

        file_problem = open(filepath_problem,"r")
        data_problem = file_problem.read()
        file_problem.close()

        file_image = open(filepath_image, "rb")
        data_image = file_image.read()
        data_image = base64.b64encode(data_image)
        # print(data_image)
        file_image.close()

        # 返回题目
        data = {
            'N': N,
            'problem_id' : data_sha,
            'data_problem': data_problem,
            'data_image': data_image.decode(),
        }
        return jsonify(data)
    elif request.method == 'POST':
        data_input = request.get_json()
        print(request.get_json())

        filepath_ans = './data/answer/' + data_input['problem_id'] + '.ans' #答案地址

        file_ans = open(filepath_ans,"r")
        data_ans = file_ans.read()
        file_ans.close()

        last_answer = data_input['answer']

        filepath_last_ans = './data/record/' + data_input['problem_id'] + '.ans' #上次提交的答案
        file_last = open(filepath_last_ans,"w")
        file_last.write(str(last_answer))
        file_last.close()

        data = {
            'answer': data_ans==data_input['answer'],
            'right_answer': data_ans,
        }
        return jsonify(data)

@app.route('/images/<filepath>', methods = ['GET'])
def download_imagess(filepath):
    return app.send_static_file(filepath)  
    return "Wrong Path"

@app.route("/download/<filepath>", methods=['GET'])
def download_file(filepath):

    file_codelist = open('list.txt','r')
    codes = file_codelist.readlines()

    for i in range(len(codes)):
        filepath_problem_this = codes[i].strip()+'.pdf'
        if filepath_problem_this == filepath:
            return app.send_static_file(filepath)  
    
    return "Wrong Path"

@app.route("/")
def index():
    return "Hello World!"

@app.route("/api", methods=['GET'])
def timenow():
    return "111"

@app.route("/problemlist", methods = ['GET'])
def problemlist():
    problems = {
        # '最短路径': '/algorithm/dijkstra'
        'algorithms':[
            {
                'problem': '单源最短路',
                'algorithm': 'dijkstra',
            },
            {
                'problem': '旅行商问题',
                'algorithm': 'fzdjf',
            },
            {
                'problem': '支撑树计数',
                'algorithm': 'treecnt',
            },
            {
                'problem': '根数计数',
                'algorithm': 'rootcnt',
            },
        ]
    }
    return jsonify(problems)


Algorithm_Type = ['单源最短路','旅行商问题','支撑树计数','根数计数']

Algorithm_Number = len(Algorithm_Type)

@app.route('/recommend', methods=['GET'])
@login_required
def recommend():
    username = current_user.id
    print("username",username)
    prblm = query_problems(username)
    print("做题记录")
    type_counter = [[0,0]] * Algorithm_Number
    cnt_all = len(prblm)
    for item in prblm:
        if item.status ==False:
            type_counter[item.problem_type][0] += 1
        else:
            type_counter[item.problem_type][1] += 1

    recommend_problems = []
    for i in range(type_counter):
        if type_counter[i][0]+type_counter[i][1]<(int)(cnt_all/Algorithm_Number):
            recommend_problems.append(i)
        if type_counter[i][0]*2>type_counter[i][1]:
            recommend_problems.append(i)
    
    return jsonify({'recommend': recommend_problems})


@app.route("/records", methods = ['GET'])
@login_required
def records():
    username = current_user.id
    print("username",username)
    prblm = query_problems(username)
    print("做题记录")
    print(prblm)
    print(prblm[0])
    data = []
    for i in range(len(prblm)):
        item = prblm[i]
        data2 ={
            'problem_id': item.problem_id,
            'username': item.username,
            'problem_type': Algorithm_Type[item.problem_type],
            'status': item.status,
        }
        print(item.id)
        print(item.username)
        print(item.problem_type)
        print(item.status)
        data.append(data2)
    return jsonify({'data':data})

@app.route("/record", methods = ['GET'])
@login_required
def get_cirten_record():
    username = current_user.id
    my_problem_id = request.args.get('problem_id')

    filepath_problem = ' ./data/problem/' + str(my_problem_id) + '.problem'
    # filepath_ans = './data/answer/' + str(my_problem_id) + '.ans'
    filepath_image = './data/image/' + str(my_problem_id) + '.ans'

    file_problem = open(filepath_problem,"r")
    data_problem = file_problem.read()
    file_problem.close()

    file_image = open(filepath_image, "rb")
    data_image = file_image.read()
    data_image = base64.b64encode(data_image)
    # print(data_image)
    file_image.close()

    # 返回题目
    data = {
        'problem_id' : my_problem_id,
        'data_problem': data_problem,
        'data_image': data_image.decode(),
    }
    return jsonify(data)

def genenrate_files():
# 进行预编译
    from run import pre_compile
    pre_compile()

    # 生成300个文件
    from run import run

    file_codelist = open('list.txt','r')

    codes = file_codelist.readlines()

    print(len(codes))

    for i in range(len(codes)):
        print(i)

        filepath_in, filepath_ans, filepath_problem = run()

        # 得到markdown并压缩
        os.system('markdown-pdf '+filepath_problem)
        filepath_pdf = './data/problem.pdf'

        # 复制并保存
        filepath_problem_this = codes[i].strip()+'.pdf'
        os.system('cp '+filepath_pdf + ' ./static/'+filepath_problem_this)

        # 复制并保存输入文件和答案
        filepath_in_this = codes[i].strip()+'.in'
        os.system('cp '+filepath_in + ' ./data/'+filepath_in_this)
        filepath_ans_this = codes[i].strip()+'.ans'
        os.system('cp '+filepath_ans + ' ./data/'+filepath_ans_this)


if __name__ == '__main__':
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.run(debug=True)

    # app.run()
