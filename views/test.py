from pathlib import Path

from flask import Blueprint, current_app
bluetest=Blueprint('test',__name__)   #蓝图的对象的名称=Blueprint('自定义蓝图名称',__name__) 

@bluetest.route('/bluetest')
def login():
    return 'bluetest'

@bluetest.route("/")
def index():
    return "Hello World!"

@bluetest.route("/api", methods=['GET'])
def timenow():
    return "111"

@bluetest.route("/access", methods=['GET'])
def accesss_count():
    count_file = Path(current_app.instance_path) / 'access_count.txt'
    count_file.parent.mkdir(parents=True, exist_ok=True)
    try:
        count = int(count_file.read_text()) + 1
    except (FileNotFoundError, ValueError):
        count = 1
    count_file.write_text(str(count))
    return str(count)
