from flask import Blueprint
blueproblem=Blueprint('problem',__name__)   #蓝图的对象的名称=Blueprint('自定义蓝图名称',__name__) 

from flask import request, jsonify
from flask_login import login_required, current_user
from app import query_problems

import base64
import os

Algorithm_Type = ['单源最短路','旅行商问题','支撑树计数','根数计数']

Algorithm_Number = len(Algorithm_Type)

@blueproblem.route('/recommend', methods=['GET'])
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


@blueproblem.route("/records", methods = ['GET'])
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

@blueproblem.route("/record", methods = ['GET'])
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

