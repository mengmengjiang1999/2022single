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

from models import Problem

def query_problems(username):
    prblm = Problem.query.filter(Problem.username == username).all()
    return prblm

def get_data_sha():
    time = datetime.timestamp(datetime.now())
    salt = random.randint(0,1000)
    data_sha = hashlib.sha256((str(time)+str(salt)).encode('utf-8')).hexdigest() 
    return data_sha 

@bluealgorithm.route('/algorithm/dijkstra', methods = ['GET', 'POST'])
def dijkstra():
    if request.method == 'GET':
        # 生成题目和答案
        data_sha = get_data_sha()

        from views.run import run
        filepath_in, filepath_ans, filepath_problem, filepath_image = run(0,data_sha)

        # 读文件
        file_problem = open(filepath_problem,"r")
        data_problem = file_problem.read()
        file_problem.close()

        # 读取图片
        file_image = open(filepath_image, "rb")
        data_image = file_image.read()
        data_image = base64.b64encode(data_image)
        file_image.close()

        # 返回题目
        data = {
            # 'N': N,
            'problem_id' : data_sha,
            'data_problem': data_problem,
            'data_image': data_image.decode(),
        }

        # 对数据库的修改，应该放在最后，保证题目生成成功了再修改
        prblm = Problem(username=current_user.id, problem_id=data_sha, problem_type=0, status = 0)
        db.session.add(prblm)
        db.session.commit()
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
