from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

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


def user_register(request):
    error = None
    success = None

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        password_confirm = request.POST.get("password_confirm", "")
        email = request.POST.get("email", "").strip()

        # 验证输入
        if not username:
            error = "用户名不能为空。"
        elif not password:
            error = "密码不能为空。"
        elif len(password) < 6:
            error = "密码长度至少为6位。"
        elif password != password_confirm:
            error = "两次输入的密码不一致。"
        elif User.objects.filter(username=username).exists():
            error = "用户名已存在，请选择其他用户名。"
        else:
            # 创建用户
            try:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email if email else ""
                )
                # 自动登录
                login(request, user)
                return redirect("/")  # 注册成功跳首页
            except Exception as e:
                error = f"注册失败：{str(e)}"

    return render(request, "core/register.html", {"error": error, "success": success})


def user_logout(request):
    logout(request)
    return redirect("/login/")
