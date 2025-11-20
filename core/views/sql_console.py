from django.shortcuts import render
from django.db import connection

def execute_sql(query: str):
    """
    执行 SQL，返回：
    - columns: 列名
    - rows: 行数据
    - error: 错误信息（如有）
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)

            # 有查询结果
            if cursor.description:
                columns = [c[0] for c in cursor.description]
                rows = cursor.fetchall()
                return {"columns": columns, "rows": rows, "error": None}

            # 无查询结果（如 UPDATE, INSERT）
            return {"columns": ["Result"], "rows": [["SQL 执行成功"]], "error": None}

    except Exception as e:
        return {"columns": [], "rows": [], "error": str(e)}


def sql_console(request):
    sql_query = ""
    result = None
    error = None

    if request.method == "POST":
        sql_query = request.POST.get("sql_query", "")
        result = execute_sql(sql_query)
        error = result["error"]

    return render(request, "core/sql_console.html", {
        "sql_query": sql_query,
        "result": result if result and not result["error"] else None,
        "error": error,
    })
