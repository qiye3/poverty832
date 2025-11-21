from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.db.models import Q
from django.core import serializers
import json
from core.permissions import get_user_permissions, TABLE_DISPLAY_NAMES
from core.models import UserTablePermission

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
        # 将权限序列化为 JSON 字符串，方便在模板中使用
        permissions_json = {}
        for key, perm in permissions.items():
            permissions_json[key] = {
                'name': perm['name'],
                'view': perm['view'],
                'edit': perm['edit'],
                'source': perm.get('source', 'role')
            }
        users_with_permissions.append({
            'user': user,
            'permissions': permissions,
            'permissions_json': json.dumps(permissions_json),
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
def set_user_table_permissions(request, user_id):
    """管理员设置用户对每张表的权限"""
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        
        # 处理每张表的权限
        for table_name in TABLE_DISPLAY_NAMES.keys():
            can_view = request.POST.get(f"view_{table_name}") == "on"
            can_edit = request.POST.get(f"edit_{table_name}") == "on"
            
            # 创建或更新权限
            UserTablePermission.objects.update_or_create(
                user=user,
                table_name=table_name,
                defaults={
                    'can_view': can_view,
                    'can_edit': can_edit,
                }
            )
        
        messages.success(request, f"用户 {user.username} 的表权限已更新")
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

