from app import app
from views.run import pre_compile

if __name__ == '__main__':
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)

    pre_compile()

    app.run()
