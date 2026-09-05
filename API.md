# API

接口返回 JSON；除登录、登录状态及明确标注的公共接口外，其余接口需要先建立登录会话。

## 用户

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| `POST` | `/login` | 登录，参数：`username`、`password` |
| `GET` | `/login_status` | 查询当前登录状态 |
| `POST` | `/logout` | 退出登录 |
| `POST` | `/regist` | 注册（当前业务配置为未开放） |

## 算法题目

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| `GET` | `/problemlist` | 获取支持的算法题型 |
| `GET` | `/algorithm?problem_type=shortestpath` | 创建或获取当前未完成题目 |
| `GET` | `/algorithm?problem_id=<id>` | 按题目编号获取本人题目 |
| `POST` | `/algorithm` | 提交答案，参数：`problem_id`、`answer` |
| `GET` | `/algorithm_fig?problem_id=<id>` | 获取本人题目图片 |
| `GET` | `/records` | 获取本人做题记录 |
| `GET` | `/record?problem_id=<id>` | 获取一条本人题目记录 |
| `GET` | `/recommend` | 根据做题情况推荐题型 |

`problem_type` 支持：`shortestpath`、`tsp`、`spantree`、`roottree`。

## 课程

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| `POST` | `/course/create` | 创建课程，参数：`coursename` |
| `POST` | `/course/remove` | 删除本人创建的课程，参数：`coursename` |
| `POST` | `/course/mycourse` | 获取本人学习和教授的课程 |
| `POST` | `/course/mystudent` | 获取课程学生，参数：`coursename` |
| `POST` | `/course/addhomework` | 添加作业，参数：`courseid`、`starttime`、`endtime`、`homework`、`count` |
| `POST` | `/course/lookhomework` | 获取课程作业及完成情况，参数：`courseid` |

## 常见状态码

- `200`：请求成功
- `400`：参数缺失或格式不正确
- `401`：未登录
- `403`：没有操作权限
- `404`：资源不存在
- `409`：资源冲突，例如课程重名
