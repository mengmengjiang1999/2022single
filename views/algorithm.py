from flask import Blueprint
bluealgorithm=Blueprint('algorithm',__name__)   #蓝图的对象的名称=Blueprint('自定义蓝图名称',__name__) 

from flask import request, jsonify

from flask_login import current_user
from sqlalchemy import and_, false, or_, true

from app import db

import random
from datetime import datetime
import hashlib
import base64

import os
import random

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

def query_problems(username):
    prblm = Problem.query.filter(Problem.username == username).all()
    return prblm
    # plm = Problem.query.filter(Problem.)

@bluealgorithm.route('/algorithm/dijkstra', methods = ['GET', 'POST'])
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

@bluealgorithm.route("/problemlist", methods = ['GET'])
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
