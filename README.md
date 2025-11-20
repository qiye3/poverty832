# 832 工程数据库系统

一个基于 Django 的贫困县数据管理系统，支持数据管理、SQL查询、AI智能查询等功能。

## 📋 目录

- [项目结构](#项目结构)
- [从零开始部署](#从零开始部署)
- [功能特性](#功能特性)
- [使用说明](#使用说明)

## 📁 项目结构

```
poverty832/
├── manage.py
├── requirements.txt
├── .env                    # 环境变量配置（需自己创建）
├── .env.example            # 环境变量示例
│
├── poverty832/             # 项目配置
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/                   # 核心应用
│   ├── models.py          # 数据模型
│   ├── views/             # 视图
│   ├── templates/         # 模板
│   ├── forms.py           # 表单
│   ├── permissions.py     # 权限系统
│   └── ai_utils.py        # AI工具
│
└── data/                   # 数据文件
    └── *.csv              # CSV数据文件
```

## 🚀 从零开始部署

### 前置要求

- Python 3.8 或更高版本
- pip（Python包管理器）

### 步骤 1：克隆项目

```bash
git clone <项目地址>
cd poverty832
```

### 步骤 2：创建虚拟环境

**Windows:**
```bash
python -m venv env
env\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv env
source env/bin/activate
```

激活成功后，命令行提示符前会显示 `(env)`。

### 步骤 3：安装依赖

```bash
pip install -r requirements.txt
```

如果下载速度慢，可以使用国内镜像：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 步骤 4：配置环境变量

在项目根目录创建 `.env` 文件（可参考 `.env.example`）：

```env
# AI 配置（可选，如果不使用AI功能可以跳过）
AI_SERVICE_TYPE=doubao
ARK_API_KEY=你的API密钥
AI_MODEL=你的模型名称或endpoint-id
```

**注意：**
- 如果不使用AI功能，可以不配置AI相关变量
- `.env` 文件已添加到 `.gitignore`，不会被提交到Git

### 步骤 5：数据库迁移

```bash
# 创建迁移文件
python manage.py makemigrations

# 执行迁移（创建数据库表）
python manage.py migrate
```

### 步骤 6：创建管理员账号

```bash
python manage.py createsuperuser
```

按提示输入：
- 用户名
- 邮箱（可选）
- 密码（输入两次）

### 步骤 7：导入数据（可选）

如果项目中有数据导入脚本，可以运行：

```bash
# 示例：导入CSV数据
python data/load_data.py
```

### 步骤 8：运行开发服务器

```bash
python manage.py runserver
```

服务器启动后，访问：
- 首页：http://127.0.0.1:8000/
- 登录页：http://127.0.0.1:8000/login/
- Django后台：http://127.0.0.1:8000/admin/

### 步骤 9：首次登录

1. 访问 http://127.0.0.1:8000/login/
2. 使用刚才创建的管理员账号登录
3. 登录后可以：
   - 查看数据表
   - 执行SQL查询
   - 使用AI智能查询
   - 管理用户和权限

## ✨ 功能特性

### 1. 数据管理
- 五张数据表的CRUD操作
- 通用列表和表单视图
- 数据统计展示

### 2. SQL查询
- 首页SQL查询
- SQL控制台
- 权限控制（禁止无权限用户执行编辑操作）

### 3. AI智能查询
- 自然语言转SQL
- 支持多种AI服务（豆包、OpenAI等）
- 可查看和编辑AI Prompt

### 4. 用户权限系统
- 用户注册和登录
- 角色管理（data_entry、analyst）
- 细粒度表级权限控制
- 管理员用户管理

### 5. 数据库详情
- 查看真实表名和列名
- SQL查询参考

## 📖 使用说明

### 用户角色

- **管理员（superuser）**：所有权限，可以管理用户和权限
- **数据录入（data_entry）**：可以查看和编辑所有表
- **分析师（analyst）**：只能查看数据，不能编辑

### 默认角色

新注册用户默认角色为 `analyst`（只有查看权限）。

### 权限管理

- 管理员可以在"用户管理"页面为每个用户单独设置每张表的权限
- 用户可以更改自己的角色（在用户详情页）

### AI配置

详细配置说明请参考：[AI_CONFIG.md](AI_CONFIG.md)

## 🔧 常见问题

### Q: 如何创建管理员？

A: 运行 `python manage.py createsuperuser`，或使用现有管理员在用户管理页面提升其他用户。

### Q: 如何配置AI？

A: 在 `.env` 文件中配置 `ARK_API_KEY` 和 `AI_MODEL`，详细说明见 `AI_CONFIG.md`。

### Q: 数据库文件在哪里？

A: SQLite数据库文件 `db.sqlite3` 在项目根目录。

### Q: 如何重置数据库？

A: 删除 `db.sqlite3` 文件，然后重新运行 `python manage.py migrate`。

## 📝 开发说明

### 运行测试

```bash
python manage.py test
```

### 收集静态文件

```bash
python manage.py collectstatic
```

### 创建新的迁移

```bash
python manage.py makemigrations
```

## 📄 许可证

本项目仅供学习和研究使用。

## 👥 贡献

欢迎提交Issue和Pull Request。

---

**提示：** 首次部署后，请使用 `python manage.py createsuperuser` 创建管理员账号。
