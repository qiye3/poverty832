项目的代码结构：

```
poverty832/
├── manage.py
│
├── poverty832/
│   ├── __init__.py
│   ├── settings.py            <-- 已改为 SQLite
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── core/
│   ├── __init__.py
│   ├── admin.py               <-- 五张表后台管理
│   ├── models.py              <-- 五张表完整结构
│   ├── urls.py                <-- 页面入口
│   ├── forms.py               <-- 通用表单
│   │
│   ├── views/
│   │   ├── __init__.py
│   │   ├── home.py            <-- 首页
│   │   ├── generic_views.py   <-- 五张表自动 CRUD（核心之一）
│   │   └── smart_query.py     <-- （可选扩展）大模型自然语言 SQL（留接口）
│   │
│   └── templates/
│       └── core/
│           ├── base.html
│           ├── home.html
│           ├── generic_list.html   <-- 通用列表页
│           ├── generic_form.html   <-- 通用表单页
│           └── result.html         <-- （大模型查询结果页面）
│
├── data/
│   ├── county_202511201906.csv
│   ├── agriculturesales_202511201906.csv
│   ├── countyeconomy_202511201906.csv
│   ├── countydemographics_202511201906.csv
│   ├── infrastructureservice_202511201905.csv
│   └── load_data.py            <-- 可运行的 CSV → SQLite 导入器
│
└── requirements.txt
```

superuser:

qiye
123
