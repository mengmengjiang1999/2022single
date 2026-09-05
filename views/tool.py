from flask import Blueprint, send_from_directory
bluetool=Blueprint('tool',__name__)   #蓝图的对象的名称=Blueprint('自定义蓝图名称',__name__) 

@bluetool.route('/images/<filepath>', methods = ['GET'])
def download_imagess(filepath):
    return send_from_directory('images', filepath)

@bluetool.route("/download/<filepath>", methods=['GET'])
def download_file(filepath):

    with open('list.txt', 'r') as file_codelist:
        codes = file_codelist.readlines()

    for i in range(len(codes)):
        filepath_problem_this = codes[i].strip()+'.pdf'
        if filepath_problem_this == filepath:
            return send_from_directory('static', filepath)
    
    return "Wrong Path"
