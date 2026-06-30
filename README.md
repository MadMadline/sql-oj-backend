# SQL Online Judge 系统

## 1 系统概述

SQL Online Judge（SQL OJ）是一个面向数据库课程的在线判题平台，支持学生在线练习 SQL 题目、参加考试，教师管理题库、组织考试并查看统计分析。系统采用前后端分离架构，判题引擎基于 Docker 沙箱实现安全隔离执行。

### 1.1 功能模块

| 模块 | 说明 |
|------|------|
| 用户管理 | 学生/教师注册登录、JWT 认证、个人信息管理 |
| 题目管理 | 题目 CRUD、难度分级、建表 SQL、批量导入 |
| 考试管理 | 创建考试、时间校验、考生范围控制、成绩排名 |
| 提交判题 | SQL 提交、Docker 沙箱执行、自动评分 |
| 统计分析 | 通过率统计、学生排名、数据概览 |

### 1.2 技术栈

**后端服务**

| 组件 | 版本 |
|------|------|
| Python | 3.10+ |
| Django | 6.0 |
| Django REST Framework | 3.17 |
| Simple JWT | 5.5 |
| MySQL | 8.x |
| PyMySQL | 1.2 |

**判题服务（独立微服务）**

| 组件 | 版本 |
|------|------|
| FastAPI | 0.115.0 |
| Docker Engine | 20.10+ |
| PostgreSQL | 15（容器内） |
| psycopg2 | 2.9.10 |

**前端**

| 组件 | 版本 |
|------|------|
| Vue | 3.5 |
| TypeScript | 6.0 |
| Vite | 8.0 |
| Element Plus | 2.14 |
| ECharts | 6.1 |

---

## 2 环境要求

在部署之前，请确保目标机器满足以下条件：

| 软件 | 最低版本 | 用途 |
|------|----------|------|
| Python | 3.10 | 后端运行环境 |
| MySQL | 8.0 | 业务数据库 |
| Docker Desktop | 20.10 | 判题沙箱 |
| Node.js | 18.0 | 前端构建与开发 |
| Git | 2.30 | 版本控制 |

操作系统：Windows 10/11 或 Linux（本文以 Windows 为例）。

---

## 3 安装与部署

### 3.1 获取源码

```powershell
git clone <仓库地址>
cd sql_oj
```

### 3.2 后端安装

```powershell
# 创建并激活虚拟环境（推荐）
python -m venv venv
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

依赖清单（requirements.txt）：
- Django >= 5.0
- djangorestframework >= 3.14
- djangorestframework-simplejwt >= 5.3
- django-cors-headers >= 4.3
- django-filter >= 23.0
- PyMySQL >= 1.1
- requests >= 2.31

### 3.3 数据库配置

**步骤一：创建数据库**

使用 MySQL 客户端执行：

```sql
CREATE DATABASE sql_oj_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**步骤二：修改配置文件**

编辑 `sql_oj/settings.py`，修改 DATABASES 配置中的连接参数：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sql_oj_db',
        'USER': 'root',
        'PASSWORD': '<你的MySQL密码>',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
```

**步骤三：执行数据库迁移**

```powershell
python manage.py migrate
```

成功后终端会输出各应用的迁移状态（均显示 OK）。

### 3.4 导入预置题目（可选）

系统内置 10 道 SQL 练习题（含建表语句和标准答案），可通过管理命令一键导入：

```powershell
python manage.py import_exercises --teacher-id=1
```

注意：需先注册一个教师账号（ID 为 1），或指定已有教师用户的 ID。

### 3.5 判题服务安装

```powershell
cd judge_service

# 安装依赖
pip install -r requirements_judge.txt
```

前置条件：Docker Desktop 已安装并正在运行。

### 3.6 前端安装

```powershell
cd sql-oj-frontend

# 安装依赖
npm install
```

---

## 4 系统启动

系统运行需要同时启动三个服务，建议按以下顺序操作（各服务使用独立终端窗口）：

### 4.1 启动判题服务

```powershell
cd judge_service
python judge_service.py
```

启动成功标志：
```
INFO:     Uvicorn running on http://0.0.0.0:8080
```

验证方法：
```powershell
curl http://localhost:8080/health
```
返回 `{"status":"ok"}` 表示正常。

### 4.2 启动后端服务

```powershell
cd sql_oj
python manage.py runserver
```

启动成功标志：
```
Starting development server at http://127.0.0.1:8000/
```

### 4.3 启动前端服务

```powershell
cd sql-oj-frontend
npm run dev
```

启动成功标志：
```
VITE vx.x.x  ready in xxx ms
Local: http://localhost:5173/
```

前端通过 Vite 代理将 `/api` 请求转发至后端 `http://localhost:8000`，无需额外配置跨域。

### 4.4 服务端口汇总

| 服务 | 地址 | 说明 |
|------|------|------|
| 后端 API | http://localhost:8000 | Django 业务后端 |
| 判题服务 | http://localhost:8080 | FastAPI 判题引擎 |
| 前端页面 | http://localhost:5173 | Vite 开发服务器 |

---

## 5 系统使用说明

### 5.1 用户注册与登录

系统支持两种角色：学生（student）和教师（teacher），注册时通过 `user_type` 字段指定。

访问前端页面 http://localhost:5173 ，在登录/注册页面完成账号创建。

<!-- [截图：注册页面] -->

### 5.2 学生端操作

#### 5.2.1 题目列表与练习

登录后进入题目列表页面，可查看所有可用题目。点击题目进入详情页，编写 SQL 并提交。

<!-- [截图：题目列表页] -->

<!-- [截图：题目详情与SQL提交页] -->

#### 5.2.2 查看提交记录

在"提交记录"页面可查看历史提交及判题结果（ACCEPTED / WRONG_ANSWER / ERROR / TIMEOUT）。

<!-- [截图：提交记录页] -->

#### 5.2.3 参加考试

在考试面板中查看当前可参加的考试。进入考试后，按题目逐一编写 SQL 并统一提交试卷。

<!-- [截图：考试面板] -->

#### 5.2.4 个人统计

在个人中心可查看：提交总数、通过数、通过率、通过题目数、最近提交记录。

<!-- [截图：学生个人统计页] -->

### 5.3 教师端操作

#### 5.3.1 题目管理

教师可进行题目的创建、编辑、删除操作。创建题目时需填写：题目标题、题目描述、难度、建表 SQL、正确答案、测试用例。

<!-- [截图：教师题目管理页] -->

<!-- [截图：创建题目表单] -->

#### 5.3.2 考试管理

教师可创建考试，设定考试名称、起止时间、选择题目并分配分值，指定参加考试的学生范围。

<!-- [截图：创建考试页] -->

<!-- [截图：考试列表与编辑] -->

#### 5.3.3 成绩统计

教师端统计页面提供：
- 整体数据概览（题目数、提交数、用户数、平均通过率）
- 每道题的通过率（尝试人数、通过人数、通过率）
- 学生通过率排名

<!-- [截图：统计分析页 - 数据概览] -->

<!-- [截图：统计分析页 - 题目通过率图表] -->

<!-- [截图：统计分析页 - 学生排名] -->

#### 5.3.4 考试成绩排名

在考试管理页面点击"排名"可查看某场考试的学生成绩排名。

<!-- [截图：考试排名页] -->

---

## 6 API 接口参考

所有接口基础地址：`http://localhost:8000`

### 6.1 认证接口（无需登录）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/auth/register/ | 用户注册 |
| POST | /api/auth/login/ | 登录，返回 JWT Token |
| POST | /api/auth/refresh/ | 刷新 Token |

### 6.2 用户管理

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | /api/users/me/ | 查看个人信息 | 登录用户 |
| PUT/PATCH | /api/users/me/ | 修改个人信息 | 登录用户 |
| GET | /api/users/me/stats/ | 个人统计数据 | 登录用户 |
| GET | /api/users/ | 用户列表 | 教师 |

### 6.3 题目管理

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | /api/questions/ | 题目列表（分页） | 登录用户 |
| POST | /api/questions/ | 创建题目 | 教师 |
| GET | /api/questions/{id}/ | 题目详情 | 登录用户 |
| PUT | /api/questions/{id}/ | 修改题目 | 教师 |
| DELETE | /api/questions/{id}/ | 删除题目 | 教师 |

### 6.4 考试管理

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | /api/exams/ | 考试列表 | 登录用户 |
| POST | /api/exams/ | 创建考试 | 教师 |
| GET | /api/exams/{id}/ | 考试详情 | 登录用户 |
| PUT | /api/exams/{id}/ | 修改考试 | 教师 |
| DELETE | /api/exams/{id}/ | 删除考试 | 教师 |
| POST | /api/exams/{id}/start/ | 开始考试 | 学生 |
| POST | /api/exams/{id}/submit/ | 提交试卷 | 学生 |
| GET | /api/exams/{id}/result/ | 考试排名 | 登录用户 |

### 6.5 提交判题

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | /api/submissions/submit/ | 提交 SQL 判题 | 登录用户 |
| GET | /api/submissions/ | 提交历史 | 登录用户 |
| GET | /api/submissions/{id}/ | 提交详情 | 登录用户 |

### 6.6 统计分析

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | /api/stats/overview/ | 整体数据概览 | 登录用户 |
| GET | /api/stats/questions/ | 题目通过率 | 教师 |
| GET | /api/stats/students/ | 学生排名 | 教师 |

---

## 7 功能验证测试

本节提供各功能模块的验证步骤，供测试人员参照执行。

### 7.1 用户注册与登录

| 步骤 | 操作 | 预期结果 |
|------|------|----------|
| 1 | 注册学生账号 | 返回 201，用户信息正确 |
| 2 | 注册教师账号 | 返回 201，user_type 为 teacher |
| 3 | 使用正确密码登录 | 返回 access 和 refresh Token |
| 4 | 使用错误密码登录 | 返回 401 |

<!-- [截图：注册成功] -->

<!-- [截图：登录成功] -->

### 7.2 题目管理（教师）

| 步骤 | 操作 | 预期结果 |
|------|------|----------|
| 1 | 教师创建题目（含建表SQL、答案、测试用例） | 返回 201，题目创建成功 |
| 2 | 查看题目列表 | 返回分页数据，每页 20 条 |
| 3 | 学生查看题目详情 | 不显示正确答案和建表 SQL |
| 4 | 教师修改题目 | 返回 200，内容更新 |
| 5 | 教师删除题目 | 返回 204，级联删除答案和测试用例 |

<!-- [截图：创建题目成功] -->

### 7.3 SQL 提交与判题

| 步骤 | 操作 | 预期结果 |
|------|------|----------|
| 1 | 学生提交正确 SQL | 返回 ACCEPTED |
| 2 | 学生提交错误 SQL | 返回 WRONG_ANSWER |
| 3 | 提交超时 SQL | 返回 TIMEOUT |
| 4 | 查看提交记录 | 包含 submission_time、question_title、execution_status |

<!-- [截图：提交正确SQL] -->

<!-- [截图：提交错误SQL] -->

### 7.4 考试流程

| 步骤 | 操作 | 预期结果 |
|------|------|----------|
| 1 | 教师创建考试（设定时间、题目、分值） | 返回 201 |
| 2 | 学生在考试时间内开始考试 | 返回题目列表 |
| 3 | 学生提交试卷（POST /api/exams/{id}/submit/） | 返回各题得分和总分 |
| 4 | 考试时间外提交 | 返回 400 错误 |
| 5 | 查看考试排名 | 按总分降序排列 |

<!-- [截图：考试中作答] -->

<!-- [截图：提交试卷结果] -->

### 7.5 统计分析（教师）

| 步骤 | 操作 | 预期结果 |
|------|------|----------|
| 1 | 查看整体概览 | 返回题目数、提交数、用户数、平均通过率 |
| 2 | 查看题目通过率 | 每题显示尝试人数、通过人数、通过率 |
| 3 | 查看学生排名 | 仅显示有提交记录的学生，含通过题目数 |

<!-- [截图：统计概览] -->

<!-- [截图：题目通过率图表] -->

<!-- [截图：学生排名表格] -->

### 7.6 权限控制

| 步骤 | 操作 | 预期结果 |
|------|------|----------|
| 1 | 未登录访问 API | 返回 401 |
| 2 | 学生尝试创建题目 | 返回 403 |
| 3 | 学生尝试创建考试 | 返回 403 |
| 4 | 学生查看他人提交记录 | 仅返回自己的记录 |

<!-- [截图：权限拦截] -->

---

## 8 项目目录结构

```
sql_oj/
├── manage.py                       # Django 管理入口
├── requirements.txt                # 后端依赖
├── sql_oj/                         # 项目配置
│   ├── settings.py                 # 数据库、JWT、CORS 等配置
│   ├── urls.py                     # 根路由
│   └── wsgi.py                     # WSGI 入口
├── apps/                           # 业务模块
│   ├── users/                      # 用户管理
│   │   ├── models.py               # 用户模型（含 user_type 角色字段）
│   │   ├── serializers.py          # 注册/用户信息序列化器
│   │   ├── views.py                # 注册、个人信息、统计
│   │   ├── permissions.py          # 自定义权限类
│   │   ├── urls.py                 # 用户路由
│   │   └── urls_auth.py            # 认证路由
│   ├── questions/                  # 题目管理
│   │   ├── models.py               # 题目、答案、测试用例模型
│   │   ├── serializers.py          # 嵌套序列化器
│   │   ├── views.py                # 题目 CRUD
│   │   ├── urls.py                 # 题目路由
│   │   └── management/commands/    # 管理命令
│   │       └── import_exercises.py # 批量导入题目
│   ├── exams/                      # 考试管理
│   │   ├── models.py               # 考试模型、考试题目关联
│   │   ├── serializers.py          # 考试序列化器
│   │   ├── views.py                # 考试 CRUD、开始考试、提交试卷、排名
│   │   └── urls.py                 # 考试路由
│   └── submissions/                # 提交判题
│       ├── models.py               # 提交记录模型
│       ├── serializers.py          # 提交记录序列化器
│       ├── views.py                # 提交与统计分析
│       ├── judge.py                # 判题服务调用
│       ├── urls.py                 # 提交路由
│       └── urls_stats.py           # 统计路由
├── judge_service/                  # 判题引擎（独立微服务）
│   ├── judge_service.py            # FastAPI 主程序（端口 8080）
│   ├── requirements_judge.txt      # 判题服务依赖
│   └── start_judge.bat             # Windows 启动脚本
├── docs/                           # 文档
│   └── judge_api.md                # 判题服务 API 文档
└── sql-oj-frontend/                # 前端（Vue 3）
    ├── package.json                # 前端依赖
    ├── vite.config.ts              # Vite 配置（含 API 代理）
    └── src/
        ├── api/                    # API 调用封装
        ├── router/                 # 路由与权限守卫
        ├── stores/                 # Pinia 状态管理
        └── views/                  # 页面组件
            ├── student/            # 学生端页面
            └── teacher/            # 教师端页面
```

---

## 9 常见问题

**Q: 执行 migrate 报错 "Access denied for user"**

A: settings.py 中的 MySQL 密码配置不正确。请确认 PASSWORD 字段与本地 MySQL root 密码一致。

**Q: 执行 migrate 报错 "Unknown database 'sql_oj_db'"**

A: 尚未创建数据库。先在 MySQL 中执行 `CREATE DATABASE sql_oj_db DEFAULT CHARACTER SET utf8mb4;`。

**Q: 提交 SQL 后返回 ERROR 或无响应**

A: 检查判题服务是否正在运行（http://localhost:8080/health），以及 Docker Desktop 是否已启动。

**Q: 前端页面无法调用后端接口**

A: 确认后端服务运行在 8000 端口，且前端 Vite 开发服务器已启动。开发环境下 API 代理已配置，无需手动处理跨域。

**Q: pip install 报错**

A: 确认 Python 版本 >= 3.10，尝试 `pip install --upgrade pip` 后重试。Windows 下 PyMySQL 一般无需编译，如遇问题可单独安装：`pip install PyMySQL`。

---

## 10 注意事项

1. `settings.py` 包含数据库密码，各成员需自行配置，不提交至版本库。
2. 后端和判题服务需同时运行，否则 SQL 提交功能不可用。
3. 判题服务依赖 Docker，首次执行判题时会拉取 PostgreSQL 镜像，请确保网络畅通。
4. 数据模型变更后需执行 `python manage.py makemigrations` 和 `python manage.py migrate`。
5. 仓库设为 Private，避免数据库密码泄露。
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
