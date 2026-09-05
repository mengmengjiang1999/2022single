# 示例数据库

`site.sample.db` 是使用当前数据库迁移创建的脱敏 SQLite 示例库。它只包含虚构数据：

- 教师账号：`sample_teacher`
- 学生账号：`sample_student`
- 两个账号的密码：`sample-pass`
- 一门示例课程、一项作业和一条已完成题目记录

邮箱使用保留域名 `example.invalid`，不包含旧数据库中的真实用户信息。

## 使用方式

先确认根目录没有需要保留的 `site.db`，再复制示例库：

```bash
cp sample/site.sample.db site.db
SECRET_KEY='local-development-secret' python manage.py
```

运行过程中请修改复制后的 `site.db`，不要直接修改仓库中的样例文件。`site.db` 已被 `.gitignore` 排除。

如需创建完全空白的数据库，请使用：

```bash
FLASK_APP=app flask init-db
```
