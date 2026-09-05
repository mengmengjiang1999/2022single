from flask import Blueprint
bluecourse=Blueprint('course',__name__)   #蓝图的对象的名称=Blueprint('自定义蓝图名称',__name__) 

from flask import request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import and_

from models import Course,CourseHomework, Problem

from models import db

@bluecourse.route('/course/create', methods=['POST'])
@login_required
def course_create():
    data_input = request.get_json(silent=True) or {}
    coursename = str(data_input.get('coursename', '')).strip()
    if not coursename:
        return jsonify({'status': False, 'error': '课程名称不能为空'}), 400

    existing_course = Course.query.filter(
        and_(
            Course.username==current_user.id, 
            Course.status == 1,
            Course.coursename == coursename
        )
    ).first()
    if existing_course is not None:
        data = {
            'status': False,
            'error': "不能创建重名课程",
        }
        return jsonify(data), 409
    else:
        course = Course(
            username=current_user.id, 
            status = 1,
            coursename = coursename
        )
        db.session.add(course)
        db.session.commit()
        data = {
            'status': True,
            'error': None
        }
        return jsonify(data)

@bluecourse.route('/course/remove', methods=['POST'])
@login_required
def course_remove():
    data_input = request.get_json(silent=True) or {}
    coursename = str(data_input.get('coursename', '')).strip()
    course = Course.query.filter(and_(Course.username==current_user.id, 
        Course.status == 1,
        Course.coursename == coursename)
    ).first()
    if course is None:
        return jsonify({'status': False, 'error': '课程不存在或没有删除权限'}), 404

    db.session.delete(course)
    db.session.commit()
    data = {
        'status': True,
        'error': None
    }
    return jsonify(data)

@bluecourse.route('/course/mycourse', methods=['POST'])
@login_required
def course_mycourse():
    username = current_user.id
    my_learn = Course.query.filter(and_(Course.username == username,Course.status==0)).all()
    learn = []
    for i in range(len(my_learn)):
        item = my_learn[i]
        data2 ={
            'id': item.id,
            'coursename': item.coursename,
        }
        learn.append(data2)

    my_teach = Course.query.filter(and_(Course.username == username,Course.status==1)).all()
    teach = []
    for i in range(len(my_teach)):
        item = my_teach[i]
        data2 ={
            'id': item.id,
            'coursename': item.coursename,
        }
        teach.append(data2)
    return jsonify({
        'status': True,
        'error': None,
        'learn': learn,
        'teach': teach
    })

@bluecourse.route('/course/mystudent', methods=['POST'])
@login_required
def course_mystudent():
    username = current_user.id
    data_input = request.get_json(silent=True) or {}
    coursename = str(data_input.get('coursename', '')).strip()
    if not coursename:
        return jsonify({'status': False, 'error': '课程名称不能为空'}), 400
    # 先查看此人是否为管理员
    is_admin = Course.query.filter(and_(
        Course.username == username,
        Course.status==1,
        Course.coursename==coursename,
        )).first()

    if is_admin is None:
        data = {
            'status':False,
            'error':"没有权限查看",
        }
        return jsonify(data)
    else:
        my_student = Course.query.filter(and_(Course.coursename == coursename,Course.status==0)).all()
        student = []
        for i in range(len(my_student)):
            item = my_student[i]
            data2 ={
                'id': item.id,
                'username': item.username, 
            }
            student.append(data2)
        return jsonify({
            'status':True,
            'error':None,
            'student':student,
        })

@bluecourse.route('/course/addhomework', methods=['POST'])
@login_required
def homework_add():
    data_input = request.get_json(silent=True) or {}
    try:
        courseid = int(data_input['courseid'])
        starttime = int(data_input['starttime'])
        endtime = int(data_input['endtime'])
        homework = int(data_input['homework'])
        count = int(data_input['count'])
    except (KeyError, TypeError, ValueError):
        return jsonify({'status': False, 'error': '作业参数无效'}), 400

    if starttime > endtime or count < 1:
        return jsonify({'status': False, 'error': '时间范围或完成次数无效'}), 400

    course = Course.query.filter(and_(
        Course.id == courseid,
        Course.username == current_user.id,
        Course.status == 1,
    )).first()
    if course is None:
        return jsonify({'status': False, 'error': '没有课程管理权限'}), 403

    course_homework = CourseHomework(
        courseid=courseid,
        homework=homework,
        starttime=starttime,
        endtime=endtime,
        count=count,
    )
    db.session.add(course_homework)
    db.session.commit()
    data = {
        'status': True,
        'error': None
    }
    return jsonify(data)

EMOJIS = ["✅","❌"]

# 同学：展示我所有的作业，以及完成情况
@bluecourse.route('/course/lookhomework', methods=['POST'])
@login_required
def homework_look():
    data_input = request.get_json(silent=True) or {}
    try:
        courseid = int(data_input['courseid'])
    except (KeyError, TypeError, ValueError):
        return jsonify({'status': False, 'error': '课程参数无效'}), 400
    # 根据课程id查找作业
    course = Course.query.get(courseid)
    if not course is None:
        membership = Course.query.filter(and_(
            Course.coursename == course.coursename,
            Course.username == current_user.id,
        )).first()
        if membership is not None:
            coursehw = CourseHomework.query.filter(
                CourseHomework.courseid == courseid
            ).all()

            coursehws = []
            for i in range(len(coursehw)):
                item = coursehw[i]
                problemrecord = Problem.query.filter(
                    and_(
                        Problem.username==current_user.id,
                        Problem.status==1,
                        Problem.problem_type==item.homework,
                        Problem.problem_time>=item.starttime,
                        Problem.problem_time<=item.endtime,
                    )
                ).all()
                finish = ""
                if len(problemrecord)>=item.count:
                    finish = EMOJIS[0]
                else:
                    finish = EMOJIS[1]
                data2 ={
                    'id': item.id,
                    'starttime': item.starttime, 
                    'endtime': item.endtime,
                    'count': item.count, 
                    'homework': item.homework, 
                    'finished': finish,
                }
                coursehws.append(data2)
            data = {
                'status': True,
                'error': None,
                'homework': coursehws,
            }
            return jsonify(data)
    data = {
        'status': False,
        'error': "没有查看权限"
    }
    return jsonify(data)
