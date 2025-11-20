from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.db.models import Q
from core.permissions import get_user_permissions

def is_admin(user):
    """检查用户是否是管理员"""
    return user.is_authenticated and user.is_superuser


@login_required
@user_passes_test(is_admin, login_url="/login/")
def user_management(request):
    """用户管理页面 - 查看所有用户"""
    # 搜索功能
    search_query = request.GET.get('search', '')
    users = User.objects.all()
    
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # 获取每个用户的权限信息
    users_with_permissions = []
    for user in users:
        permissions = get_user_permissions(user)
        users_with_permissions.append({
            'user': user,
            'permissions': permissions,
            'groups': user.groups.all(),
        })
    
    # 获取所有可用的组
    all_groups = Group.objects.all()
    
    context = {
        'users_with_permissions': users_with_permissions,
        'all_groups': all_groups,
        'search_query': search_query,
    }
    
    return render(request, "core/user_management.html", context)


@login_required
@user_passes_test(is_admin, login_url="/login/")
def change_user_role(request, user_id):
    """管理员更改用户角色"""
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        group_id = request.POST.get("group_id")
        
        if group_id:
            try:
                group = Group.objects.get(id=group_id)
                # 清除用户的所有组
                user.groups.clear()
                # 添加新组
                user.groups.add(group)
                messages.success(request, f"用户 {user.username} 的角色已更改为：{group.name}")
            except Group.DoesNotExist:
                messages.error(request, "选择的角色不存在")
        else:
            # 如果group_id为空，则清除所有角色
            user.groups.clear()
            messages.success(request, f"用户 {user.username} 的角色已清除")
        
        return redirect("user_management")
    
    return redirect("user_management")


@login_required
@user_passes_test(is_admin, login_url="/login/")
def toggle_admin(request, user_id):
    """管理员提升/取消用户的管理员权限"""
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        
        # 不能取消自己的管理员权限
        if user.id == request.user.id:
            messages.error(request, "不能取消自己的管理员权限")
        else:
            if user.is_superuser:
                user.is_superuser = False
                user.is_staff = False
                user.save()
                messages.success(request, f"用户 {user.username} 的管理员权限已取消")
            else:
                user.is_superuser = True
                user.is_staff = True
                user.save()
                messages.success(request, f"用户 {user.username} 已提升为管理员")
        
        return redirect("user_management")
    
    return redirect("user_management")


@login_required
@user_passes_test(is_admin, login_url="/login/")
def delete_user(request, user_id):
    """管理员删除用户"""
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        
        # 不能删除自己
        if user.id == request.user.id:
            messages.error(request, "不能删除自己的账号")
        else:
            username = user.username
            user.delete()
            messages.success(request, f"用户 {username} 已删除")
        
        return redirect("user_management")
    
    return redirect("user_management")

