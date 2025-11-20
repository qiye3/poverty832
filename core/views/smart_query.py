from django.shortcuts import render
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.ai_utils import ask_ai_sql, get_full_prompt
from core.permissions import can_execute_sql

def execute_sql(query: str):
    """执行 SQL 并返回结果"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [c[0] for c in cursor.description] if cursor.description else []
            rows = cursor.fetchall()
            rowcount = len(rows) if rows else cursor.rowcount
        return {"columns": columns, "rows": rows, "error": None, "rowcount": rowcount}
    except Exception as e:
        return {"columns": [], "rows": [], "error": str(e), "rowcount": 0}


@login_required(login_url="/login/")
def smart_query(request):
    ai_query = ""
    ai_sql = ""
    result = None
    explanation = ""
    error = None

    if request.method == "POST":
        ai_query = request.POST.get("ai_query", "")
        
        if not ai_query.strip():
            messages.warning(request, "查询内容不能为空")
        else:
            # 1. 让 AI 生成 SQL + 解释
            ai_sql, explanation = ask_ai_sql(ai_query)

            # 如果 SQL 为空，直接报错
            if not ai_sql:
                error = "AI 未能生成有效 SQL，请尝试换一种提问方式。"
                messages.error(request, f"❌ {error}")
            else:
                # 2. 检查权限
                can_execute, perm_error = can_execute_sql(request.user, ai_sql)
                if not can_execute:
                    error = perm_error
                    messages.error(request, f"❌ 权限错误：{perm_error}")
                else:
                    # 3. 执行 SQL
                    sql_result = execute_sql(ai_sql)

                    if sql_result["error"]:
                        error = sql_result["error"]
                        messages.error(request, f"❌ SQL 执行失败：{error}")
                    else:
                        result = sql_result
                        row_count = len(result.get("rows", []))
                        messages.success(request, f"✅ AI 查询执行成功！返回 {row_count} 行数据")

    # 获取prompt信息（用于显示）
    prompt_info = None
    if ai_query:
        prompt_info = get_full_prompt(ai_query)
    
    return render(request, "core/smart_query.html", {
        "ai_query": ai_query,
        "ai_sql": ai_sql,
        "result": result,
        "explanation": explanation,
        "error": error,
        "prompt_info": prompt_info,
    })
