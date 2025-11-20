from django.shortcuts import render
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.permissions import can_execute_sql

def execute_sql(query: str):
    """
    执行 SQL，返回：
    - columns: 列名
    - rows: 行数据
    - error: 错误信息（如有）
    - rowcount: 受影响的行数（对于UPDATE/INSERT/DELETE）
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)

            # 有查询结果
            if cursor.description:
                columns = [c[0] for c in cursor.description]
                rows = cursor.fetchall()
                return {
                    "columns": columns, 
                    "rows": rows, 
                    "error": None,
                    "rowcount": len(rows)
                }

            # 无查询结果（如 UPDATE, INSERT, DELETE）
            rowcount = cursor.rowcount
            return {
                "columns": ["Result"], 
                "rows": [["SQL 执行成功"]], 
                "error": None,
                "rowcount": rowcount
            }

    except Exception as e:
        return {"columns": [], "rows": [], "error": str(e), "rowcount": 0}


@login_required(login_url="/login/")
def sql_console(request):
    sql_query = ""
    result = None
    error = None

    if request.method == "POST":
        sql_query = request.POST.get("sql_query", "")
        
        if not sql_query.strip():
            messages.warning(request, "SQL 查询不能为空")
        else:
            # 检查权限
            can_execute, perm_error = can_execute_sql(request.user, sql_query)
            if not can_execute:
                messages.error(request, f"❌ 权限错误：{perm_error}")
                error = perm_error
            else:
                result = execute_sql(sql_query)
                error = result["error"]
                
                if error:
                    messages.error(request, f"❌ SQL 执行失败：{error}")
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

    return render(request, "core/sql_console.html", {
        "sql_query": sql_query,
        "result": result if result and not result["error"] else None,
        "error": error,
    })
