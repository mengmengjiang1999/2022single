from flask import Blueprint
bluetest=Blueprint('user',__name__)   #蓝图的对象的名称=Blueprint('自定义蓝图名称',__name__) 

@bluetest.route('/bluetest')
def login():
    return 'bluetest'