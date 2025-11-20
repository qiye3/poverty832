from django.contrib.auth.decorators import user_passes_test

def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

def data_entry_required(view_func):
    return user_passes_test(lambda u: u.groups.filter(name="data_entry").exists())(view_func)

def analyst_required(view_func):
    return user_passes_test(lambda u: u.groups.filter(name="analyst").exists())(view_func)


# ---------------------------
# 表级权限检查
# ---------------------------

# 表名映射
TABLE_MODEL_MAP = {
    'county': 'County',
    'infra': 'InfrastructureService',
    'agri': 'AgricultureSales',
    'economy': 'CountyEconomy',
    'demo': 'CountyDemographics',
}

TABLE_DISPLAY_NAMES = {
    'county': 'County（县域）',
    'infra': '基础设施',
    'agri': '农业销售',
    'economy': '经济指标',
    'demo': '人口结构',
}


def has_table_view_permission(user, table_name):
    """检查用户是否有查看表的权限"""
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    # 所有登录用户都可以查看
    return True


def has_table_edit_permission(user, table_name):
    """检查用户是否有编辑表的权限（包括新增、修改、删除）"""
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    # data_entry 组有编辑权限
    if user.groups.filter(name="data_entry").exists():
        return True
    # analyst 组只有查看权限
    return False


def get_user_permissions(user):
    """获取用户对所有表的权限"""
    permissions = {}
    for table_key, table_display in TABLE_DISPLAY_NAMES.items():
        permissions[table_key] = {
            'name': table_display,
            'view': has_table_view_permission(user, table_key),
            'edit': has_table_edit_permission(user, table_key),
        }
    return permissions


def can_execute_sql(user, sql_query):
    """检查用户是否可以执行SQL语句（检查是否有编辑操作）"""
    if not user or not user.is_authenticated:
        return False, "未登录用户不能执行SQL"
    
    sql_upper = sql_query.strip().upper()
    
    # 检查是否包含编辑操作
    edit_keywords = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'CREATE', 'TRUNCATE']
    has_edit_operation = any(keyword in sql_upper for keyword in edit_keywords)
    
    if has_edit_operation:
        # 只有管理员或data_entry可以执行编辑操作
        if user.is_superuser or user.groups.filter(name="data_entry").exists():
            return True, None
        else:
            return False, "您没有执行编辑操作的权限（INSERT/UPDATE/DELETE等）。请联系管理员获取数据录入权限。"
    
    # 查询操作所有登录用户都可以执行
    return True, None