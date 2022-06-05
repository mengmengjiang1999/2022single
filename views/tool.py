from flask import Blueprint
bluetool=Blueprint('tool',__name__)   #蓝图的对象的名称=Blueprint('自定义蓝图名称',__name__) 

@bluetool.route('/images/<filepath>', methods = ['GET'])
def download_imagess(filepath):
    return bluetool.send_static_file(filepath)  
    return "Wrong Path"

@bluetool.route("/download/<filepath>", methods=['GET'])
def download_file(filepath):

    file_codelist = open('list.txt','r')
    codes = file_codelist.readlines()

    for i in range(len(codes)):
        filepath_problem_this = codes[i].strip()+'.pdf'
        if filepath_problem_this == filepath:
            return bluetool.send_static_file(filepath)  
    
    return "Wrong Path"