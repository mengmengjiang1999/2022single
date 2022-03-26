from flask import Flask, escape, url_for, request, render_template, jsonify

import sys
import os

# from flask_sqlalchemy import SQLAlchemy  # 导入扩展类

app = Flask(__name__)

# @app.route('/algorithm/dijkstra')
# def dijkstra():
#     if request.method == 'GET':
#         N = request.form['N']

#         from run import run

#         filepath_in, filepath_ans, filepath_problem = run()

#         file_in = open(filepath_in,"r")
#         data_in = file_in.read()
#         file_in.close()

#         file_ans = open(filepath_ans,"r")
#         data_ans = file_ans.read()
#         file_ans.close()

#         file_problem = open(filepath_problem,"r")
#         data_problem = file_problem.read()
#         file_problem.close()

#         data = {
#             'N': N,
#             'data_in': data_in,
#             'data_ans': data_ans,
#             'data_problem': data_problem,
#         }
#         return jsonify(data)
#     elif request.method == 'POST':
#         return 'haha'


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

    app.run()
