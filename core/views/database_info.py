from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from core.models import (
    County, InfrastructureService, AgricultureSales,
    CountyEconomy, CountyDemographics
)
from core.permissions import TABLE_DISPLAY_NAMES

@login_required
def database_info(request):
    """数据库详情页，显示每个表的真实表名和列名"""
    
    # 模型映射
    MODEL_MAP = {
        'county': County,
        'infra': InfrastructureService,
        'agri': AgricultureSales,
        'economy': CountyEconomy,
        'demo': CountyDemographics,
    }
    
    tables_info = []
    
    for table_key, model in MODEL_MAP.items():
        # 获取真实表名
        table_name = model._meta.db_table
        
        # 获取所有数据库字段信息
        fields_info = []
        # 使用 _meta.fields 获取所有数据库字段（不包括ManyToMany和反向关系）
        for field in model._meta.fields:
            # 获取数据库列名
            db_column = field.db_column if hasattr(field, 'db_column') and field.db_column else field.column
            
            field_info = {
                'name': field.name,  # 模型字段名
                'db_column': db_column,  # 数据库列名
                'type': field.get_internal_type() if hasattr(field, 'get_internal_type') else 'Unknown',
                'null': getattr(field, 'null', False),
                'blank': getattr(field, 'blank', False),
                'primary_key': getattr(field, 'primary_key', False),
            }
            
            # 如果是外键，添加关联表信息
            # 使用 remote_field.model 获取关联模型（更可靠）
            if hasattr(field, 'remote_field') and field.remote_field is not None:
                related_model = field.remote_field.model
                if related_model is not None:
                    field_info['type'] = 'ForeignKey'
                    field_info['related_table'] = related_model._meta.db_table
            
            fields_info.append(field_info)
        
        tables_info.append({
            'key': table_key,
            'display_name': TABLE_DISPLAY_NAMES.get(table_key, table_key),
            'table_name': table_name,
            'model_name': model.__name__,
            'fields': fields_info,
        })
    
    context = {
        'tables_info': tables_info,
    }
    
    return render(request, "core/database_info.html", context)

