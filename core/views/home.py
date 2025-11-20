from django.shortcuts import render
from django.db import connection
from django.db.models import Avg, Sum
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import (
    County, InfrastructureService, AgricultureSales,
    CountyEconomy, CountyDemographics
)
from core.permissions import can_execute_sql
from core.ai_utils import ask_ai_sql


def run_sql(query: str):
    """执行 SQL 并返回表格格式结果"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description] if cursor.description else []
            rows = cursor.fetchall()
            rowcount = len(rows) if rows else cursor.rowcount
        return {"columns": columns, "rows": rows, "error": None, "rowcount": rowcount}
    except Exception as e:
        return {"columns": ["error"], "rows": [[str(e)]], "error": str(e), "rowcount": 0}



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
        if not sql_query.strip():
            messages.warning(request, "SQL 查询不能为空")
        else:
            # 检查权限
            can_execute, perm_error = can_execute_sql(request.user, sql_query)
            if not can_execute:
                messages.error(request, f"❌ 权限错误：{perm_error}")
                result = {"columns": ["错误"], "rows": [[perm_error]], "error": perm_error}
            else:
                result = run_sql(sql_query)
                if result.get("error"):
                    messages.error(request, f"❌ SQL 执行失败：{result['error']}")
                else:
                    # 判断是查询还是修改操作
                    sql_upper = sql_query.strip().upper()
                    if any(keyword in sql_upper for keyword in ['SELECT', 'SHOW', 'DESCRIBE', 'EXPLAIN']):
                        row_count = result.get("rowcount", len(result.get("rows", [])))
                        messages.success(request, f"✅ SQL 查询执行成功！返回 {row_count} 行数据")
                    else:
                        row_count = result.get("rowcount", 0)
                        if row_count > 0:
                            messages.success(request, f"✅ SQL 执行成功！影响 {row_count} 行数据")
                        else:
                            messages.success(request, "✅ SQL 执行成功！")

    # --------------------------
    # AI 查询
    # --------------------------
    if request.method == "POST" and "ai_query" in request.POST:
        ai_query = request.POST.get("ai_query")
        if not ai_query.strip():
            messages.warning(request, "查询内容不能为空")
        else:
            # 1. 让 AI 生成 SQL + 解释
            ai_sql, explanation = ask_ai_sql(ai_query)
            
            # 如果 SQL 为空，直接报错
            if not ai_sql:
                error_msg = explanation or "AI 未能生成有效 SQL，请尝试换一种提问方式。"
                messages.error(request, f"❌ {error_msg}")
                result = {"columns": ["错误"], "rows": [[error_msg]], "error": error_msg}
            else:
                # 2. 检查权限
                can_execute, perm_error = can_execute_sql(request.user, ai_sql)
                if not can_execute:
                    messages.error(request, f"❌ 权限错误：{perm_error}")
                    result = {"columns": ["错误"], "rows": [[perm_error]], "error": perm_error}
                else:
                    # 3. 执行 SQL
                    result = run_sql(ai_sql)
                    
                    if result.get("error"):
                        messages.error(request, f"❌ SQL 执行失败：{result['error']}")
                    else:
                        row_count = result.get("rowcount", len(result.get("rows", [])))
                        messages.success(request, f"✅ AI 查询执行成功！返回 {row_count} 行数据")
                        if explanation:
                            messages.info(request, f"💡 AI说明：{explanation}")

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
