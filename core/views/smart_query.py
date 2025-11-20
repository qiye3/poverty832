from django.shortcuts import render
from django.db import connection
from core.ai_utils import ask_doubao_sql

def execute_sql(query: str):
    """执行 SQL 并返回结果"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [c[0] for c in cursor.description] if cursor.description else []
            rows = cursor.fetchall()
        return {"columns": columns, "rows": rows, "error": None}
    except Exception as e:
        return {"columns": [], "rows": [], "error": str(e)}


def smart_query(request):
    ai_query = ""
    ai_sql = ""
    result = None
    explanation = ""
    error = None

    if request.method == "POST":
        ai_query = request.POST.get("ai_query", "")

        # 1. 让 Doubao 生成 SQL + 解释
        ai_sql, explanation = ask_doubao_sql(ai_query)

        # 如果 SQL 为空，直接报错
        if not ai_sql:
            error = "AI 未能生成有效 SQL，请尝试换一种提问方式。"
        else:
            # 2. 执行 SQL
            sql_result = execute_sql(ai_sql)

            if sql_result["error"]:
                error = sql_result["error"]
            else:
                result = sql_result

    return render(request, "core/smart_query.html", {
        "ai_query": ai_query,
        "ai_sql": ai_sql,
        "result": result,
        "explanation": explanation,
        "error": error,
    })
