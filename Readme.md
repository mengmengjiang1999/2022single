# Readmd



运行方式：

本单机版app已经升级为功能齐全的后端
```shell
python3 manage.py


flask init-db --drop
```

其他数据库操作：

https://segmentfault.com/a/1190000041646505


下面的启动命令已作废
```shell
python3 run.py

python3 app.py
```

每次运行可以随机生成一个题目。题面地址为`'./data/problem.md'`，题目用到的图片地址为`'./images/dijkstra.png'`，答案地址为`'./data/data.ans'`。

此外还有：

```shell
filepath_exe = './algorithm/shortestpath/program/main' #可执行文件地址
filepath_code = './algorithm/shortestpath/program/dijkstra.cpp' #代码地址
```

以上内容都可以在`run.py`中进行修改。


<!-- zip -e 2022.zip ./data/problem.md ./images/dijkstra.png

zip -e 2022.zip ./data/problem.pdf
2022
2022 -->

ssh mengmengjiang@166.111.7.121

<!-- gunicorn -w 4 -b 166.111.7.121:5000 app:app -->

http://166.111.7.121/download/fb7929605a5d613883397bd2cf9284d30694f3d5.pdf

<!-- sudo vim /etc/nginx/sites-available/default -->


sudo vim /etc/nginx/sites-available/default
sudo nginx -t
gunicorn -w 4 -b 127.0.0.1:5000 app:app 


nohup gunicorn -w 4 -b 127.0.0.1:5000 app:app &

ps -e | grep gunicorn

部署参考资料：
（最好用的）
https://blog.csdn.net/william_munch/article/details/103368580
（second）
https://www.jianshu.com/p/d607ca5718a5
（third）
https://dormousehole.readthedocs.io/en/latest/deploying/wsgi-standalone.html

关于flask数据库的使用方法
https://www.geeksforgeeks.org/connect-flask-to-a-database-with-flask-sqlalchemy/


关于OJ的数学公式怎么敲
https://www.bbsmax.com/A/rV57pNadPD/

<!-- ```
python3
>>> from app import db
>>> db.create_all()
>>> exit()

pip3 install Flask-Migrate

flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```
 -->

```
运行前可以选择是否要删库重建
正式发布后不得使用此命令
flask initdb
```


<!-- 关于登录注册 -->

https://www.cnblogs.com/hhh5460/p/9745812.html

http://www.ityouknow.com/python/2019/11/13/python-web-flask-login-057.html

pip3 install flask-login

<!-- 关于分文件 -->

flask蓝图
https://cloud.tencent.com/developer/article/1648137

<!-- 关于nginx -->

mengmengjiang:2022single chenzm$ cat /usr/local/etc/nginx/nginx.conf

#user  nobody;
worker_processes  1;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;

    server {
        listen       8080;
        server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        #location / {
        #    root   html;
        #    index  index.html index.htm;
        #}
        location / {
            proxy_pass http://localhost:2333/;
            proxy_redirect off;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            #以下代码使支持WebSocket
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
       }

        location /api/ {
            proxy_pass http://localhost:5000/;
            proxy_redirect off;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            #以下代码使支持WebSocket
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
       }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }

        # proxy the PHP scripts to Apache listening on 127.0.0.1:80
        #
        #location ~ \.php$ {
        #    proxy_pass   http://127.0.0.1;
        #}

        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
        #
        #location ~ \.php$ {
        #    root           html;
        #    fastcgi_pass   127.0.0.1:9000;
        #    fastcgi_index  index.php;
        #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
        #    include        fastcgi_params;
        #}

        # deny access to .htaccess files, if Apache's document root
        # concurs with nginx's one
        #
        #location ~ /\.ht {
        #    deny  all;
        #}
    }


    # another virtual host using mix of IP-, name-, and port-based configuration
    #
    #server {
    #    listen       8000;
    #    listen       somename:8080;
    #    server_name  somename  alias  another.alias;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}


    # HTTPS server
    #
    #server {
    #    listen       443 ssl;
    #    server_name  localhost;

    #    ssl_certificate      cert.pem;
    #    ssl_certificate_key  cert.key;

    #    ssl_session_cache    shared:SSL:1m;
    #    ssl_session_timeout  5m;

    #    ssl_ciphers  HIGH:!aNULL:!MD5;
    #    ssl_prefer_server_ciphers  on;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}
    include servers/*;
}

nginx启动：
sudo nginx