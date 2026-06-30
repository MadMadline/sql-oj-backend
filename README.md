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

**Q：前端调用 API 报 CORS 错误？**
A：开发阶段 `CORS_ALLOW_ALL_ORIGINS = True` 已经配好了。如果还报错，检查前端请求 URL 是否正确。

**Q：在哪里查看 API 文档？**
A：启动后端后，浏览器访问 `http://127.0.0.1:8000/api/`，DRF 自带的浏览界面可以直接测试所有接口。
