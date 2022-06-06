from flask import Blueprint

from views.problem import ALGORITHM_TYPE
bluealgorithm=Blueprint('algorithm',__name__)   #蓝图的对象的名称=Blueprint('自定义蓝图名称',__name__) 

from flask import request, jsonify

from flask_login import current_user, login_required
from sqlalchemy import and_, false, null, or_, true

from app import db

import random
from datetime import datetime
import hashlib
import base64

import os
import random

from models import Problem

def get_data_sha():
    time = datetime.timestamp(datetime.now())
    salt = random.randint(0,1000)
    data_sha = hashlib.sha256((str(time)+str(salt)).encode('utf-8')).hexdigest() 
    return data_sha 

def run_algorithm_get(type:int,data_sha:str,need_run:bool=False):
    from views.run import run
    filepath_in, filepath_ans, filepath_problem, filepath_image = run(type,data_sha,need_run)
    
    print(data_sha)
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
        'problem_id' : data_sha,
        'data_problem': data_problem,
        'data_image': data_image.decode(),
    }

    return data

def run_algorithm_post(data_input:str):
    filepath_ans = './data/answer/' + data_input['problem_id'] + '.ans' #答案地址

    file_ans = open(filepath_ans,"r")
    data_ans = file_ans.read()
    file_ans.close()

    last_answer = data_input['answer']

    filepath_last_ans = './data/record/' + data_input['problem_id'] + '.ans' #上次提交的答案
    file_last = open(filepath_last_ans,"w")
    file_last.write(str(last_answer))
    file_last.close()

    print(data_ans)

    data = {
        'answer': data_ans==data_input['answer'],
        'right_answer': data_ans,
    }

    print(data)
    return data

@bluealgorithm.route('/algorithm', methods = ['GET', 'POST'])
@login_required
def algorithm():
    if request.method == 'GET':
        data_input = request.args
        problem_id = data_input.get('problem_id')
        print(problem_id)

        if not problem_id:
            curr_problem_type = 0

            if data_input.get('problem_type') == 'shortestpath':
                curr_problem_type = 0
            elif data_input.get('problem_type') == 'tsp':
                curr_problem_type = 1
            elif data_input.get('problem_type') == 'spancount':
                curr_problem_type = 2
            elif data_input.get('problem_type') == 'rootcount':
                curr_problem_type = 3
            else:
                return jsonify({
                'status' : "FAIL" 
            })

            # 这个时候不能直接就来创造新的题目，还需要检查是否有未完成的题目
            prblm = Problem.query.filter(
                and_(Problem.problem_type==curr_problem_type,
                Problem.username==current_user.id,Problem.status!=1)).first()
            print(prblm)
            if prblm is None:
                # 新题目的标志
                data_sha = get_data_sha()

                # 得到一份新题目
                data = run_algorithm_get(0,data_sha,True)

                # 对数据库的修改，应该放在最后，保证题目生成成功了再修改
                prblm = Problem(
                    username=current_user.id, 
                    problem_time = datetime.timestamp(datetime.now()),
                    problem_id=data_sha, 
                    problem_type=curr_problem_type, 
                    status = 0
                )
                db.session.add(prblm)
                db.session.commit()
                return jsonify(data)
            else:
                # 该用户还有未完成的题目
                data_sha = prblm.problem_id
                # 取读取数据了
                data = run_algorithm_get(0,data_sha,False)
                return jsonify(data)
        else:
            data_sha = problem_id
            # 那么这就是取读取数据了
            data = run_algorithm_get(0,data_sha,False)
            return jsonify(data)
        
    elif request.method == 'POST':
        data_input = request.get_json()
        print(request.get_json())
        data = run_algorithm_post(data_input)
        curr_problem_id = data_input['problem_id']

        print("curr_problem_id",curr_problem_id)

        prblm = Problem.query.filter(
            Problem.problem_id==curr_problem_id).first()

        prblm.problem_time = datetime.timestamp(datetime.now())
        # 对数据库的修改，应该放在最后，保证题目生成成功了再修改

        for item in data:
            print(item)

        if data['answer']==True:
            prblm.status = 1
        else:
            prblm.status = 2
        db.session.commit()

        return jsonify(data)

@bluealgorithm.route("/problemlist", methods = ['GET'])
@login_required
def problemlist():
    problems = {
        # '最短路径': '/algorithm/dijkstra'
        'algorithms':[
            {
                'id':'P1000',
                'problem_name': '单源最短路',
                'problem_type': 'shortestpath',
                'algorithm': 'dijkstra',
            },
            {
                'id':'P1001',
                'problem_name': '旅行商问题',
                'problem_type': 'tsp',
                'algorithm': 'fzdjf',
            },
            {
                'id':'P1002',
                'problem_name': '支撑树计数',
                'problem_type': 'spantree',
                'algorithm': 'treecnt',
            },
            {
                'id':'P1003',
                'problem_name': '根数计数',
                'problem_type': 'roottree',
                'algorithm': 'rootcnt',
            },
        ]
    }
    return jsonify(problems)
