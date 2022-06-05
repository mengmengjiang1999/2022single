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