from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from tools import stringToBase64,base64ToString

# from flask_sqlalchemy import SQLAlchemy  # 导入扩展类

app = Flask(__name__)

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
 
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

# Import for Migrations
from flask_migrate import Migrate, migrate
 
# Settings for migrations
migrate = Migrate(app, db)

# login

app.secret_key= '23232333'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


from views.user import blueuser,Userinfo
from views.algorithm import bluealgorithm,query_problems
from views.tool import bluetool
from views.test import bluetest
from views.problem import blueproblem

app.register_blueprint(blueuser)
app.register_blueprint(bluealgorithm)
app.register_blueprint(bluetool)
app.register_blueprint(bluetest)
app.register_blueprint(blueproblem)

from werkzeug.security import generate_password_hash

import click

@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息

if __name__ == '__main__':
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.run(debug=True)

    # app.run()
