from flask import Flask

from flask_sqlalchemy import SQLAlchemy

# from flask_sqlalchemy import SQLAlchemy  # 导入扩展类
 
# Creating an SQLAlchemy instance
db = SQLAlchemy()

class Userinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(256), unique=False)
    email = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return '<User %r>' % self.username

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column()
    username = db.Column(db.String(80), unique=False)
    problem_id = db.Column(db.String(120), unique=True, nullable=False)
    problem_type = db.Column(db.Integer, unique=False, nullable=False)
    status = db.Column(db.Integer, unique=False, nullable=False)
    # status: 0:还未做，1:做了答案正确，2：做了，答案错误
    problem_time = db.Column(db.Integer, unique=False, nullable=False)
    # 表示题目创建的时间，或上次提交答案的时间
 
    def __repr__(self):
        return "id : {self.id}, problem_id: {self.problem_id}, status: {self.status}"

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coursename = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True)
    status = db.Column(db.Integer, unique=False, nullable=False)
    # 0:普通用户
    # 1:管理员

    def __repr__(self):
        return "id : {self.id}, problem_id: {self.problem_id}, status: {self.status}"

class CourseHomework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coursename = db.Column(db.String(80), unique=False, nullable=False)
    homework = db.Column(db.Integer, unique=False, nullable=True)
    # 作业的开始时间和结束时间
    starttime = db.Column(db.Integer, unique=False, nullable=False)
    endtime = db.Column(db.Integer, unique=False, nullable=False)
    # 该题目需要完成的次数
    count = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return "id : {self.id}, problem_id: {self.problem_id}, status: {self.status}"