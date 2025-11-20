from django import template
register = template.Library()

@register.filter
def attr(obj, attr_name):
    return getattr(obj, attr_name)

@register.filter
def in_group(user, group_name):
    """检查用户是否在指定的组中"""
    if not user or not user.is_authenticated:
        return False
    return user.groups.filter(name=group_name).exists()