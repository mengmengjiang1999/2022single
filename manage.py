from app import app

if __name__ == '__main__':
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.run(debug=True)

    # app.run()
