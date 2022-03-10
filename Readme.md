# Readmd

运行方式：

```shell
./python3 run.py
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

<!-- ssh mengmengjiang@166.111.7.121 -->

<!-- gunicorn -w 4 -b 166.111.7.121:5000 app:app -->
<!-- http://166.111.7.121/download/fb7929605a5d613883397bd2cf9284d30694f3d5.pdf -->

<!-- sudo vim /etc/nginx/sites-available/default -->

 sudo vim /etc/nginx/sites-available/default
 sudo nginx -t
 gunicorn -w 4 -b 0.0.0.0:5000 app:app 


nohup gunicorn -w 2 -b 127.0.0.1:5000 app:app &

ps -e | grep gunicorn


https://blog.csdn.net/william_munch/article/details/103368580