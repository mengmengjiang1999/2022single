import os
from flask import Blueprint
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
    with open("access_count.txt", "r+") as f:
        count = f.read()
        if not count:
            count = 1
        else:
            count = int(count) + 1
        print("Access count:", count)
        f.seek(0)
        f.write(str(count))
    return str(count)

if not os.path.exists("access_count.txt"):
    with open("access_count.txt", "w") as f:
        f.write("0")
