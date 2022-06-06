import json
from turtle import home
from flask import Blueprint
bluecourse=Blueprint('course',__name__)   #蓝图的对象的名称=Blueprint('自定义蓝图名称',__name__) 

from flask import request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import and_, false, null, or_, true

from models import Course,CourseHomework

from app import db

@bluecourse.route('/course/create', methods=['POST'])
@login_required
def course_create():
    data_input = request.get_json()
    coursename = data_input['coursename']
    course1 = Course.query.filter(
        and_(
            Course.username==current_user.id, 
            Course.status == 0,
            Course.coursename == coursename
        )
    ).all()
    if not course1 is None:
        data = {
            'status': False,
            'error': "不能创建重名课程",
        }
        return jsonify(data)
    else:
        course = Course(
            username=current_user.id, 
            status = 0,
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
    data_input = request.get_json()
    coursename = data_input['coursename']
    course = Course.query.filter(and_(Course.username==current_user.id, 
        Course.status == 0,
        Course.coursename == coursename)
    ).first()
    db.session.remove(course)
    db.session.commit()
    data = {
        'status': False,
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
    data_input = request.get_json()
    coursename = data_input['coursename']
    # 先查看此人是否为管理员
    is_admin = Course.query.filter(and_(
        Course.username == username,
        Course.status==0,
        Course.coursename==coursename,
        )).first()

    if not is_admin is None:
        data = {
            'status':False,
            'error':"没有权限查看",
        }
        return jsonify(data)
    else:
        my_student = Course.query.filter(and_(Course.coursename == coursename,Course.status==1)).all()
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
    data_input = request.get_json()
    courseid = int(data_input['courseid'])
    starttime = data_input['starttime']
    endtime = data_input['endtime']
    homework = data_input['homework']
    count = data_input['count']
    course = Course(
        courseid == courseid,
        homework == homework,
        starttime == starttime,
        endtime == endtime,
        count == count,
    )
    db.session.add(course)
    db.session.commit()
    data = {
        'status': True,
        'error': None
    }
    return jsonify(data)


# 同学：展示我所有的作业，以及完成情况
@bluecourse.route('/course/lookhomework', methods=['POST'])
@login_required
def homework_add():
    data_input = request.get_json()
    courseid = int(data_input['courseid'])
    # 根据课程id查找作业
    course = Course.query.get(courseid)
    if not course is None:
        if course.username == current_user.id:
            coursehw = CourseHomework.query.filter(
                CourseHomework.courseid == courseid
            ).all()
            coursehws = []
            for i in range(len(coursehw)):
                item = coursehw[i]
                data2 ={
                    'id': item.id,
                    'starttime': item.starttime, 
                    'endtime': item.endtime,
                    'count': item.count, 
                    'homework': item.homework, 
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