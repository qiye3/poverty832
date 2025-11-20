from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def user_login(request):
    error = None

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("/")  # 登录成功跳首页
        else:
            error = "用户名或密码错误。"

    return render(request, "core/login.html", {"error": error})


def user_logout(request):
    logout(request)
    return redirect("/login/")
