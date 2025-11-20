from django.shortcuts import render
from django.db import connection
from django.db.models import Avg, Sum
from django.contrib.auth.decorators import login_required
from core.models import (
    County, InfrastructureService, AgricultureSales,
    CountyEconomy, CountyDemographics
)
from core.permissions import can_execute_sql


def run_sql(query: str):
    """执行 SQL 并返回表格格式结果"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description] if cursor.description else []
            rows = cursor.fetchall()
        return {"columns": columns, "rows": rows, "error": None}
    except Exception as e:
        return {"columns": ["error"], "rows": [[str(e)]], "error": str(e)}



@login_required(login_url="/login/")
def home(request):
    sql_query = ""
    ai_query = ""
    result = None

    # --------------------------
    # SQL 查询执行
    # --------------------------
    if request.method == "POST" and "sql_query" in request.POST:
        sql_query = request.POST.get("sql_query")
        # 检查权限
        can_execute, perm_error = can_execute_sql(request.user, sql_query)
        if not can_execute:
            result = {"columns": ["错误"], "rows": [[perm_error]], "error": perm_error}
        else:
            result = run_sql(sql_query)

    # --------------------------
    # AI 查询（预留）
    # --------------------------
    if request.method == "POST" and "ai_query" in request.POST:
        ai_query = request.POST.get("ai_query")
        result = {"columns": ["AI 暂未接入"], "rows": [[ai_query]]}

    # --------------------------
    # 快速入口
    # --------------------------
    quick_links = [
        {"title": "County", "icon": "🏙", "url": "/county/"},
        {"title": "Infra", "icon": "🛣", "url": "/infra/"},
        {"title": "Agriculture", "icon": "🌾", "url": "/agri/"},
        {"title": "Economy", "icon": "💹", "url": "/economy/"},
        {"title": "Demo", "icon": "👥", "url": "/demo/"},
    ]

    # --------------------------
    # Dashboard 数据统计（使用 Django ORM 正确方式）
    # --------------------------
    stats = [
        {"label": "县域数量", 
         "value": County.objects.count()},

        {"label": "平均 GDP（亿元）", 
         "value": round(CountyEconomy.objects.aggregate(avg=Avg("gdp_total"))["avg"] or 0, 2)},

        {"label": "总人口数", 
         "value": CountyDemographics.objects.aggregate(s=Sum("population_total"))["s"] or 0},

        {"label": "平均宽带覆盖率（%）", 
         "value": round(InfrastructureService.objects.aggregate(avg=Avg("broadband_coverage"))["avg"] or 0, 2)},
    ]

    return render(request, "core/home.html", {
        "quick_links": quick_links,
        "stats": stats,
        "sql_query": sql_query,
        "ai_query": ai_query,
        "result": result,
    })
