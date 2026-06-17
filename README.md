# zw-021 琴行教务管理系统

音乐培训机构一体化教务管理：教师、学员、课程、教室、排课、报名、上课记录、考级、乐器、用户权限。

## 技术栈

- 后端：Python 3.9 + FastAPI + SQLAlchemy + PyMySQL
- 前端：Vue 3 + Vite + Element Plus + Pinia + Vue Router

## 快速启动

### 1. 初始化数据库

创建 MySQL 数据库并执行初始化脚本：

```bash
mysql -u root -p < backend/sql/init.sql
```

### 2. 启动后端

```bash
cd backend
cp .env.example .env
pip install -r requirements.txt
python run.py
```

后端默认运行在 http://localhost:8000。

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端默认运行在 http://localhost:5173。

## 默认账号

- 管理员：`admin / admin123`
- 教师：`teacher / teacher123`

## 构建

```bash
cd frontend
npm run build
```

构建产物位于 `frontend/dist`。
