from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from core.permissions import get_user_permissions, TABLE_DISPLAY_NAMES

@login_required
def user_profile(request):
    """用户详情页，显示权限信息"""
    user = request.user
    permissions = get_user_permissions(user)
    
    # 获取用户当前所在的组
    user_groups = user.groups.all()
    
    # 确保默认组存在，如果不存在则创建
    default_groups = ['data_entry', 'analyst']
    for group_name in default_groups:
        Group.objects.get_or_create(name=group_name)
    
    # 获取所有组
    all_groups = Group.objects.all()
    
    context = {
        'user': user,
        'permissions': permissions,
        'user_groups': user_groups,
        'all_groups': all_groups,
    }
    
    return render(request, "core/user_profile.html", context)


@login_required
def change_role(request):
    """用户更改角色"""
    if request.method == "POST":
        group_id = request.POST.get("group_id")
        
        try:
            group = Group.objects.get(id=group_id)
            # 清除用户的所有组
            request.user.groups.clear()
            # 添加新组
            request.user.groups.add(group)
            messages.success(request, f"角色已更改为：{group.name}")
        except Group.DoesNotExist:
            messages.error(request, "选择的角色不存在")
        
        return redirect("user_profile")
    
    return redirect("user_profile")

