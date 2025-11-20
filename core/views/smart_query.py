from django.shortcuts import render
from django.db import connection

def smart_query(request):
    result = None
    sql_error = None
    query_text = ""

    if request.method == "POST":
        query_text = request.POST.get("query")

        try:
            with connection.cursor() as cursor:
                cursor.execute(query_text)
                result = cursor.fetchall()
        except Exception as e:
            sql_error = str(e)

    return render(request, "core/result.html", {
        "query_text": query_text,
        "result": result,
        "error": sql_error
    })
