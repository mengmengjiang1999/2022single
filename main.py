from flask import Flask, escape, url_for, request, render_template, jsonify

import sys
import os

from flask_sqlalchemy import SQLAlchemy  # 导入扩展类

app = Flask(__name__)

@app.route('/algorithm/dijkstra')
def dijkstra():
    if request.method == 'GET':
        N = request.form['N']

        from run import run

        filepath_in, filepath_ans, filepath_problem = run()

        file_in = open(filepath_in,"r")
        data_in = file_in.read()
        file_in.close()

        file_ans = open(filepath_ans,"r")
        data_ans = file_ans.read()
        file_ans.close()

        file_problem = open(filepath_problem,"r")
        data_problem = file_problem.read()
        file_problem.close()

        data = {
            'N': N,
            'data_in': data_in,
            'data_ans': data_ans,
            'data_problem': data_problem,
        }
        return jsonify(data)
    elif request.method == 'POST':
        return 'haha'

# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('hello', next='/'))
#     print(url_for('profile', username='John Doe'))


if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run(debug = True)

    # 进行预编译
    from run import pre_compile
    pre_compile()

    # 生成300个文件