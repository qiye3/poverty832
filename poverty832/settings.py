"""
Django settings for poverty832 project.
"""

from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# ================================
# AI 配置
# ================================
# AI服务类型：'doubao'（豆包/火山方舟）、'openai'（OpenAI）、'custom'（自定义OpenAI兼容API）
AI_SERVICE_TYPE = os.getenv("AI_SERVICE_TYPE", "doubao")

# AI API密钥（从环境变量读取，支持多种环境变量名）
AI_API_KEY = os.getenv("AI_API_KEY") or os.getenv("DOUBAO_API_KEY") or os.getenv("ARK_API_KEY")

# AI API基础URL（可选，如果不设置则使用默认值）
AI_API_BASE = os.getenv("AI_API_BASE", None)

# AI模型名称/Endpoint（可选，如果不设置则使用默认值）
AI_MODEL = os.getenv("AI_MODEL", None)

# 向后兼容
DOUBAO_API_KEY = AI_API_KEY

# ===============================
# BASE_DIR
# ===============================
BASE_DIR = Path(__file__).resolve().parent.parent

# ===============================
# 基本配置
# ===============================
SECRET_KEY = "django-insecure-change-this-to-anything-for-dev"
DEBUG = True
ALLOWED_HOSTS = []
LOGIN_URL = "/login/"


# ===============================
# 已安装的应用
# ===============================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 主业务 APP
    'core',
]


# ===============================
# 中间件
# ===============================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'poverty832.urls'


# ===============================
# TEMPLATES 设置
# ===============================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # 如果你使用全局模板，可以在这里加 BASE_DIR / "templates"
        'APP_DIRS': True,   # 允许 Django 自动查找 core/templates/
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'poverty832.wsgi.application'


# ===============================
# 数据库：SQLite
# ===============================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}


# ===============================
# 密码校验（默认即可）
# ===============================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ===============================
# 国际化（使用中文时区）
# ===============================
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = False


# ===============================
# 静态文件
# ===============================
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# ===============================
# 默认主键类型
# ===============================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
