# SQL OJ 项目

SQL 在线判题系统（SQL Online Judge），包含 Django 后端（API + 判题引擎）和 Vue 3 前端。

---

## 一、项目概述

本项目是一个类 LeetCode 数据库题的在线判题平台：

- **学生端**：练习 SQL 题目、参加考试、提交 SQL 代码、查看成绩排名
- **教师端**：创建/管理题目、组织考试、查看学生成绩统计
- **判题引擎**：Docker 沙箱执行学生提交的 SQL ✅ 已完成

---

## 二、目前已完成的功能

### 2.1 用户系统
- ✅ 学生和教师使用同一张表，通过 `user_type` 字段区分
- ✅ 注册接口：`POST /api/auth/register/`
- ✅ 登录接口：`POST /api/auth/login/`，返回 JWT Token（有效期 2 小时）
- ✅ Token 刷新接口：`POST /api/auth/refresh/`
- ✅ 查看/修改个人信息：`GET/PUT /api/users/me/`
- ✅ 个人统计：`GET /api/users/me/stats/` — 提交数、通过率、最近提交
- ✅ 教师查看学生列表：`GET /api/users/` — 显示所有学生（用于分配考试等）
- ✅ 权限控制：教师才能管理题目和考试，学生只能提交自己的答案

### 2.2 题目管理
- ✅ 教师创建题目（包含题目描述、正确答案 SQL、测试用例）
- ✅ 题目列表（支持分页，每页 20 条）
- ✅ 查看题目详情（含所有正确答案和测试用例）
- ✅ 修改题目（同步更新答案和测试用例）
- ✅ 删除题目（级联删除关联的答案和测试用例）
- ✅ 难度分级：Easy / Medium / Hard
- ✅ 题目名称：新增 `title` 字段，区分简短名称和完整题干
- ✅ 批量导入：预置了 10 道上机课习题（含建表 SQL 和标准答案），一键导入数据库
- ✅ 学生不可见答案：学生查看题目时自动隐藏正确答案 SQL 和建表语句

### 2.3 考试管理
- ✅ 教师创建考试（设定开始/结束时间、总分、题目分配）
- ✅ 考试范围：支持"所有学生"或"指定学生"（M2M 关联）
- ✅ 考试列表（教师只看自己创建的考试，学生看全体开放 + 自己被指定的考试）
- ✅ 学生开始考试（自动校验是否在考试时间窗口内）
- ✅ 查看考试结果与排名
- ✅ 编辑考试时返回题目标题和真实ID（方便前端展示）
- ✅ 创建/编辑考试时验证题目ID合法性（无效ID返回400而非500）

### 2.4 提交与判题
- ✅ 学生提交 SQL 代码
- ✅ 判题服务对接已完成（FastAPI + Docker + PostgreSQL，真实执行 SQL 并比对结果）
- ✅ 提交历史查询（学生只看自己的，教师可查看所有学生的提交记录）
- ✅ 考试模式下自动校验时间
- ✅ 提交记录包含 `question_title`、`submission_time` 字段，支持查看详情

### 2.5 统计分析
- ✅ 整体数据概览（题目数、提交数、用户数、平均通过率）
- ✅ 每道题的通过率统计（按学生维度：尝试人数/通过人数/通过率）
- ✅ 学生通过率排名（含通过题目数，仅返回有提交记录的学生）
- ✅ 个人统计：学生端返回 `passed_questions`（通过题目数）；教师端返回管理题目数、考试数

### 2.6 前端页面 ✅ 已完成
- ✅ 登录 / 注册页面
- ✅ 学生端：题目列表、题目详情、提交记录、考试面板
- ✅ 教师端：题目管理（CRUD）、创建考试、成绩统计（ECharts 可视化）
- ✅ 路由守卫：自动区分学生/教师角色，未登录跳转登录页
- ✅ API 代理：Vite 开发代理自动转发 `/api` 到后端 8000 端口

---

## 三、技术栈

| 技术 | 说明 |
|------|------|
| Django 6.0 | Web 框架 |
| Django REST Framework 3.17 | API 框架 |
| Simple JWT 5.5 | JWT 身份认证 |
| PyMySQL 1.2 | MySQL 数据库驱动 |
| django-cors-headers 4.9 | 跨域请求支持（前端调用需要） |
| django-filter 25.2 | API 筛选/搜索支持 |
| MySQL 8.x | 关系型数据库 |

### 判题服务（独立微服务）

| 技术 | 说明 |
|------|------|
| FastAPI | 判题服务 Web 框架 |
| Docker | 启动临时 PostgreSQL 容器作为沙箱 |
| PostgreSQL 15 | 沙箱数据库（每个提交独立容器） |
| psycopg2 | Python 连接 PostgreSQL |

### 前端

| 技术 | 说明 |
|------|------|
| Vue 3 + TypeScript | 前端框架 |
| Vite 8 | 构建工具 |
| Element Plus | UI 组件库 |
| Pinia | 状态管理 |
| Vue Router 5 | 路由 |
| Axios | HTTP 请求 |
| ECharts 6 | 图表可视化 |

---

## 四、项目目录结构

```
sql_oj/
├── manage.py                  # Django 管理入口
├── requirements.txt           # 业务后端依赖列表
├── .gitignore                 # Git 忽略规则
├── README.md                  # 本文件
│
├── sql_oj/                    # 项目配置目录
│   ├── settings.py            # 数据库、JWT、DRF、CORS 等所有配置
│   ├── urls.py                # 根路由（API 网关，所有接口入口）
│   └── wsgi.py                # WSGI 入口
│
├── apps/                      # 业务模块目录
│   ├── users/                 # 用户管理模块
│   │   ├── models.py          # 用户数据模型
│   │   ├── serializers.py     # 序列化器（注册、用户信息）
│   │   ├── views.py           # 视图（注册、个人信息、用户列表）
│   │   ├── permissions.py     # 权限类（教师权限、管理员权限）
│   │   ├── urls.py            # 用户管理路由
│   │   └── urls_auth.py       # 认证相关路由（注册/登录/刷新）
│   │
│   ├── questions/             # 题目管理模块
│   │   ├── models.py          # 题目、答案、测试用例模型
│   │   ├── serializers.py     # 序列化器（支持嵌套创建）
│   │   ├── views.py           # 视图（CRUD + 批量创建答案/用例）
│   │   ├── urls.py            # 题目管理路由
│   │   └── management/        # Django 管理命令
│   │       └── commands/
│   │           └── import_exercises.py   # 批量导入 10 道上机课题目的命令
│   │
│   ├── exams/                 # 考试管理模块
│   │   ├── models.py          # 考试、考试题目关联模型
│   │   ├── serializers.py     # 序列化器
│   │   ├── views.py           # 视图（CRUD + 时间校验 + 排名）
│   │   └── urls.py            # 考试管理路由
│   │
│   └── submissions/           # 提交判题模块
│       ├── models.py          # 提交记录模型
│       ├── serializers.py     # 序列化器
│       ├── views.py           # 视图（提交 SQL + 统计分析）
│       ├── judge.py           # 判题服务对接（调用判题微服务）
│       ├── urls.py            # 提交记录路由
│       └── urls_stats.py      # 统计分析路由
│
├── judge_service/             # 判题引擎（独立微服务）
│   ├── judge_service.py       # 判题主程序（FastAPI，端口 8080）
│   ├── requirements_judge.txt # 判题服务依赖
│   └── start_judge.bat        # Windows 一键启动脚本
│
├── docs/                      # 文档
│   └── judge_api.md           # 判题服务 API 详细文档
│
└── sql-oj-frontend/           # 前端项目（Vue 3 + TS）
    ├── package.json           # 前端依赖
    ├── vite.config.ts         # Vite 配置（含 /api 代理）
    └── src/
        ├── router/index.ts    # 路由 + 权限守卫
        ├── stores/user.ts     # 用户状态（Pinia）
        ├── api/               # 后端 API 调用封装
        └── views/             # 页面组件
            ├── student/       # 学生端页面
            └── teacher/       # 教师端页面
```

---

## 五、队友拿到代码后怎么用

### 5.1 前置条件

**你的电脑上需要安装：**

1. **Python 3.10 或更高版本**
   - 下载地址：https://www.python.org/downloads/
   - 安装时**勾选 "Add Python to PATH"**

2. **MySQL 8.x**
   - 下载地址：https://dev.mysql.com/downloads/installer/
   - 安装时记住 root 密码
   - 确保 MySQL 服务正在运行

### 5.2 克隆代码并安装依赖

打开终端（PowerShell 或 CMD），执行以下命令：

```powershell
# 1. 克隆仓库（把 URL 换成实际的）
git clone https://github.com/你的用户名/sql-oj-backend.git
cd sql-oj-backend

# 2. 创建虚拟环境（可选但推荐）
python -m venv venv

# 3. 激活虚拟环境
# Windows PowerShell:
venv\Scripts\activate
# Windows CMD:
venv\Scripts\activate.bat

# 4. 安装依赖
pip install -r requirements.txt
```

### 5.3 配置数据库

**第一步：创建数据库**

打开 MySQL 命令行或图形工具（如 Navicat、DBeaver、MySQL Workbench），执行：

```sql
CREATE DATABASE sql_oj_db DEFAULT CHARACTER SET utf8mb4;
```

**第二步：修改配置文件**

打开 `sql_oj/settings.py`，找到这段代码，把密码改成你自己的 MySQL 密码：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sql_oj_db',
        'USER': 'root',
        'PASSWORD': '你的MySQL密码',  # ← 改这里
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
```

### 5.4 初始化数据库表

```powershell
# 在项目根目录（有 manage.py 的那个目录）执行：
python manage.py migrate
```

看到一堆 "OK" 就说明成功了。

### 5.5 启动判题服务 ⚠️ 重要

**判题服务必须单独启动**，否则提交 SQL 时会失败。

前置条件：需要安装 **Docker Desktop**（https://www.docker.com/products/docker-desktop/）

```powershell
# 1. 进入判题服务目录
cd judge_service

# 2. 安装判题服务依赖
pip install -r requirements_judge.txt

# 3. 启动判题服务（新开一个终端窗口）
python judge_service.py
# 或双击 start_judge.bat
```

看到以下输出说明判题服务启动成功：
```
INFO:     Uvicorn running on http://0.0.0.0:8080
```

验证判题服务是否正常：
```powershell
# 在另一个终端里执行
curl http://localhost:8080/health
# 返回 {"status":"ok"} 即正常
```

### 5.6 启动后端服务

```powershell
python manage.py runserver
```

看到以下输出说明启动成功：

```
Starting development server at http://127.0.0.1:8000/
```

现在你可以用浏览器访问 `http://127.0.0.1:8000/api/` 查看所有可用的 API 接口（DRF 自带的浏览界面）。

> ⚠️ 注意：后端和判题服务**需要同时运行**（两个终端窗口），否则提交 SQL 会报错。

### 5.7 启动前端 ⚠️ 新增

**前置条件：** Node.js 18+ （https://nodejs.org/）

```powershell
# 1. 进入前端目录
cd sql-oj-frontend

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm run dev
```

默认运行在 `http://localhost:5173`，Vite 配置了代理，`/api` 请求会自动转发到 `http://localhost:8000`。

> 💡 **推荐启动顺序**：先启动判题服务（5.5），再启动后端（5.6），最后启动前端（5.7）。

### 5.8 测试一下接口

用 **Postman**（https://www.postman.com/downloads/）或浏览器的开发者工具测试：

**注册一个教师账号：**

```
POST http://127.0.0.1:8000/api/auth/register/
Content-Type: application/json

{
    "username": "laoshi_wang",
    "email": "wang@school.edu.cn",
    "password": "123456",
    "user_type": "teacher"
}
```

**登录获取 Token：**

```
POST http://127.0.0.1:8000/api/auth/login/
Content-Type: application/json

{
    "username": "laoshi_wang",
    "password": "123456"
}
```

返回结果里有一个 `access` 字段，这就是你的 JWT Token。之后调用所有 API 时，需要在请求头里加上：

```
Authorization: Bearer 你的token
```

---

## 六、完整 API 接口列表

> 所有接口基础地址：`http://127.0.0.1:8000`

### 6.1 认证接口（不需要登录）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/auth/register/` | 用户注册 |
| POST | `/api/auth/login/` | 用户登录，返回 JWT Token |
| POST | `/api/auth/refresh/` | 刷新过期的 Token |

### 6.2 用户管理（需要登录）

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/users/me/` | 查看自己的信息 | 本人 |
| PUT | `/api/users/me/` | 修改自己的信息 | 本人 |
| GET | `/api/users/me/stats/` | 查看个人统计数据 | 本人 |
| GET | `/api/users/` | 查看用户列表（教师看到所有学生） | 教师 |
| GET | `/api/users/{id}/` | 查看指定用户 | 教师/本人 |

### 6.3 题目管理

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/questions/` | 题目列表（分页） | 登录即可 |
| POST | `/api/questions/` | 创建题目 | 教师 |
| GET | `/api/questions/{id}/` | 查看题目详情 | 登录即可 |
| PUT | `/api/questions/{id}/` | 修改题目 | 教师 |
| DELETE | `/api/questions/{id}/` | 删除题目 | 教师 |

**创建题目示例：**

```json
POST /api/questions/
Authorization: Bearer <token>

{
    "title": "查询学生",
    "description": "查询所有学生的姓名和年龄",
    "difficulty": "easy",
    "sample_input": "无",
    "sample_output": "Alice | 20",
    "create_table_sql": "CREATE TABLE students(id INT, name VARCHAR(50), age INT);",
    "answers": [
        {"correct_sql": "SELECT name, age FROM students;"}
    ],
    "test_cases": [
        {"test_input": "", "expected_output": "name|age\nAlice|20\nBob|22"}
    ]
}
```

### 6.4 考试管理

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/exams/` | 考试列表 | 登录即可 |
| POST | `/api/exams/` | 创建考试 | 教师 |
| GET | `/api/exams/{id}/` | 考试详情 | 登录即可 |
| PUT | `/api/exams/{id}/` | 修改考试 | 教师 |
| DELETE | `/api/exams/{id}/` | 删除考试 | 教师 |
| POST | `/api/exams/{id}/start/` | 开始考试 | 学生 |
| GET | `/api/exams/{id}/result/` | 考试排名 | 登录即可 |

**创建考试示例：**

```json
POST /api/exams/
Authorization: Bearer <token>

{
    "title": "期末 SQL 考试",
    "start_time": "2026-06-01T08:00:00+08:00",
    "end_time": "2026-06-01T10:00:00+08:00",
    "total_score": 100,
    "exam_questions": [
        {"question": 1, "score": 30},
        {"question": 2, "score": 70}
    ]
}
```

### 6.5 提交判题

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | `/api/submissions/submit/` | 提交 SQL | 登录即可 |
| GET | `/api/submissions/` | 查看提交历史 | 登录即可 |
| GET | `/api/submissions/{id}/` | 查看某次提交详情 | 登录即可 |

**提交 SQL 示例：**

```json
POST /api/submissions/submit/
Authorization: Bearer <token>

{
    "question_id": 1,
    "exam_id": null,
    "submitted_sql": "SELECT name, age FROM students;"
}
```

### 6.6 统计分析

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/stats/overview/` | 整体数据概览 | 登录即可 |
| GET | `/api/stats/questions/` | 每道题的通过率 | 教师 |
| GET | `/api/stats/students/` | 学生通过率排名 | 教师 |

---

## 七、判题引擎（已完成 ✅）

### 架构说明

判题引擎是一个**独立的微服务**，代码在 `judge_service/` 目录下。

**工作流程：**
1. 学生通过业务后端提交 SQL
2. 业务后端调用判题服务（`POST http://localhost:8080/judge`）
3. 判题服务用 Docker 启动一个临时 PostgreSQL 容器
4. 执行建表语句 → 插入测试数据 → 执行学生 SQL → 比对结果
5. 返回判题结果，销毁临时容器

**安全机制：**
- 容器隔离：每个提交独立容器，执行完立即销毁
- 资源限制：内存 512MB、CPU 配额限制
- SQL 超时：30 秒超时自动中断
- 权限裁剪：移除 SYS_ADMIN、NET_RAW 等高危权限
- 事务回滚：每个测试用例独立会话，执行后回滚

### 修改判题服务地址

如果判题服务不在本机，或端口不同，修改 `apps/submissions/judge.py` 第 4 行：

```python
JUDGE_SERVICE_URL = "http://实际地址:实际端口/judge"
```

### 详细 API 文档

判题服务的完整 API 文档见：[docs/judge_api.md](docs/judge_api.md)

---

## 八、前端项目说明

前端代码在 `sql-oj-frontend/` 目录下，技术栈为 Vue 3 + TypeScript + Element Plus。

### 页面路由一览

| 路径 | 页面 | 角色 |
|---|---|---|
| `/login` | 登录 | 所有人 |
| `/questions` | 题目列表 | 学生 / 教师 |
| `/questions/:id` | 题目详情 + 提交 | 学生 / 教师 |
| `/submissions` | 提交记录 | 学生 / 教师 |
| `/exam/:id` | 考试面板 | 学生 |
| `/teacher/questions` | 题目管理 | 教师 |
| `/teacher/questions/create` | 创建题目 | 教师 |
| `/teacher/exams` | 考试管理 | 教师 |
| `/teacher/stats` | 成绩统计 | 教师 |

### 关键设计

1. **后端地址**：前端通过 Vite proxy 转发 `/api` 到 `http://localhost:8000`，无需配置跨域
2. **认证流程**：登录后 Token 和用户信息存入 localStorage，路由守卫自动校验
3. **角色区分**：学生端无布局栏直接浏览，教师端带侧边栏 Layout
4. **统计图表**：教师统计页使用 ECharts 渲染通过率排名等图表

---

## 九、注意事项

### 9.1 关于数据库密码
`settings.py` 里的 MySQL 密码是明文写的（目前是 `123456`）。你们组内使用没问题，但**不要把这个项目设为 Public（公开）仓库**，否则别人能看到你的数据库密码。建议用 **Private（私有）仓库**。

### 9.2 关于数据库表
- 所有表都是 Django 自动创建的，**不要手动去 MySQL 里建表或改表**
- 如果改了 models.py，需要执行：
  ```powershell
  python manage.py makemigrations
  python manage.py migrate
  ```

### 9.3 ⚠️ 本次更新后队友需要做的（重要）

**本次更新包含数据库迁移（Exam 新增 student_scope 和 students 字段）和多个后端 Bug 修复。拉取代码后请执行：**

```powershell
# 1. 拉取最新代码
git pull origin main

# 2. 修改 sql_oj/settings.py 中的数据库密码为你自己的 MySQL 密码

# 3. 执行数据库迁移（Exam 表新增 student_scope + students M2M）
python manage.py migrate

# 4. 如果之前没导入题目，执行导入
python manage.py import_exercises --teacher-id=1
```

**本次后端修复内容：**

1. **考试编辑时外键约束 500 错误** → 新增题目ID验证，无效ID返回 400 + 明确错误信息
2. **教师看不到学生提交记录** → 修复过滤逻辑，教师可查看所有学生的提交
3. **GET /api/stats/students/ 返回空** → 改用 Exists 子查询，确保正确返回有提交的学生
4. **GET /api/stats/questions/ 通过率不准** → 改为按学生维度统计（尝试人数/通过人数）
5. **GET /api/stats/overview/ 缺少平均通过率** → 新增 `average_pass_rate` 字段
6. **学生"通过题目数"为 0** → GET /api/users/me/stats/ 新增 `passed_questions` 字段
7. **编辑考试时题目只显示序号** → ExamQuestionSerializer 新增 `question_title`、`question_id`
8. **ExamSerializer 字段冲突** → 修复 `students` M2M 写入冲突，考试可正确设置学生范围

> ⚠️ 注意：`settings.py` 不在本次提交中（每人密码不同），拉取后需自行配置密码。

### 9.4 关于虚拟环境
- 建议每个人都在自己电脑上创建虚拟环境（`python -m venv venv`）
- 虚拟环境目录 `venv/` 已加入 `.gitignore`，不会被上传到 GitHub

### 9.5 关于代码提交
- **不要直接在 main 分支上改代码**
- 每个人新建自己的分支：
  ```powershell
  git checkout -b 你的分支名
  ```
- 功能完成后，在 GitHub 网页上发起 Pull Request 合并到 main

### 9.6 批量导入上机课题目

项目内置了 10 道上机课习题，每道题都有 `title`（标题）和 `description`（完整题干），建表 SQL 和标准答案都已经写好。导入方法：

```powershell
# 先注册一个教师账号（如果还没有）
# POST /api/auth/register/ → {"username":"teacher","email":"t@t.com","password":"123456","user_type":"teacher"}

# 执行导入（教师 ID 默认为 1）
python manage.py import_exercises --teacher-id=1
```

成功后会输出每道题的导入信息，一共 10 道题（easy 4 道、medium 3 道、hard 3 道）。

题目数据在：[apps/questions/management/commands/import_exercises.py](apps/questions/management/commands/import_exercises.py)

> 💡 如果之前导入过旧版本（没有 `title`），需要先删除旧数据再重新导入：见 [9.3](#93-⚠️-本次更新后队友需要做的important)

### 9.7 常见问题

**Q：运行 `python manage.py migrate` 报错 "Access denied for user"？**
A：MySQL 密码没配对。检查 `settings.py` 里的 PASSWORD。

**Q：运行 `python manage.py migrate` 报错 "Unknown database 'sql_oj_db'"？**
A：还没有创建数据库。先去 MySQL 里执行 `CREATE DATABASE sql_oj_db DEFAULT CHARACTER SET utf8mb4;`

**Q：运行 `pip install -r requirements.txt` 报错安装失败？**
A：尝试用 pip 单独安装失败的包。如果 PyMySQL 装不上，试试 `pip install PyMySQL --user`

**Q：前端调用 API 报 CORS 错误？**
A：开发阶段 `CORS_ALLOW_ALL_ORIGINS = True` 已经配好了。如果还报错，检查前端请求 URL 是否正确。

**Q：在哪里查看 API 文档？**
A：启动后端后，浏览器访问 `http://127.0.0.1:8000/api/`，DRF 自带的浏览界面可以直接测试所有接口。
