# 2022single

一个基于 Flask 的单机在线评测（OJ）后端，包含用户、课程、题目、算法生成器和测试相关接口。

## 环境要求

- Python 3.9（项目中的部分依赖版本较旧，建议使用与原项目一致的 Python 版本）
- C++ 编译器（用于预编译 `algorithm/` 下的示例程序）
- Node.js/npm（仅在需要前端依赖时使用）

## 本地运行

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py
```

应用默认使用仓库根目录下的本地 SQLite 数据库 `site.db`。首次运行前可初始化数据库：

```bash
flask --app app init-db
```

如需删除已有表并重新创建（会清空本地数据）：

```bash
flask --app app init-db --drop
```

## 前端依赖

仓库不跟踪 `node_modules/`。如需安装 `package.json` 中声明的依赖，请运行：

```bash
npm ci
```

## 项目结构

- `app.py`：Flask 应用配置、蓝图注册和数据库初始化命令
- `manage.py`：本地启动入口，启动前预编译算法程序
- `views/`：用户、课程、题目、算法和工具接口
- `models.py`：数据库模型
- `migrations/`：数据库迁移文件
- `algorithm/`：题目生成器与 C++ 示例程序
- `templates/`：页面模板
- `data/`：题目模板及运行时数据目录
- `images/dijkstra.png`：最短路示例题使用的固定图片

## 仓库约定

依赖目录、Python 缓存、本地数据库、运行时生成的题目图片和下载 PDF 均由 `.gitignore` 排除。提交代码前可用下面的命令确认工作区：

```bash
git status
```

接口说明见 [API.md](API.md)。各算法目录下的 `Readme.md` 包含对应生成器说明。
