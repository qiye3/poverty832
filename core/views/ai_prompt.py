from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from core.models import AIPromptConfig
from core.ai_utils import get_full_prompt

def is_admin(user):
    """检查用户是否是管理员"""
    return user.is_authenticated and user.is_superuser


@login_required
def view_prompt(request):
    """用户查看AI Prompt"""
    prompt_config = AIPromptConfig.get_config()
    
    context = {
        'prompt_config': prompt_config,
    }
    
    return render(request, "core/view_prompt.html", context)


@login_required
@user_passes_test(is_admin, login_url="/login/")
def edit_prompt(request):
    """管理员编辑AI Prompt"""
    prompt_config = AIPromptConfig.get_config()
    
    if request.method == "POST":
        prompt_config.table_schema = request.POST.get("table_schema", "")
        prompt_config.system_prompt = request.POST.get("system_prompt", "")
        prompt_config.user_prompt_template = request.POST.get("user_prompt_template", "")
        prompt_config.updated_by = request.user
        prompt_config.save()
        
        messages.success(request, "AI Prompt配置已更新")
        return redirect("edit_prompt")
    
    context = {
        'prompt_config': prompt_config,
    }
    
    return render(request, "core/edit_prompt.html", context)

