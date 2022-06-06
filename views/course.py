from flask import Blueprint
bluecourse=Blueprint('course',__name__)   #蓝图的对象的名称=Blueprint('自定义蓝图名称',__name__) 

from flask import request, jsonify
from flask_login import login_required, current_user

from models import Course