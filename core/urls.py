from django.urls import path

from .views.home import home
from .views.smart_query import smart_query
from .views.generic_views import (
    CountyListView, CountyCreateView, CountyUpdateView,
    InfraListView, InfraCreateView, InfraUpdateView,
    AgriListView, AgriCreateView, AgriUpdateView,
    EconomyListView, EconomyCreateView, EconomyUpdateView,
    DemoListView, DemoCreateView, DemoUpdateView
)
from .views.sql_console import sql_console
from .views.auth import user_login, user_logout, user_register
from .views.user_profile import user_profile, change_role
from .views.admin_views import user_management, change_user_role, toggle_admin, delete_user, set_user_table_permissions
from .views.database_info import database_info
from .views.ai_prompt import view_prompt, edit_prompt


urlpatterns = [
    # 首页
    path('', home, name="home"),

    # County
    path('county/', CountyListView.as_view(), name="county_list"),
    path('county/add/', CountyCreateView.as_view(), name="county_add"),
    path('county/<int:pk>/edit/', CountyUpdateView.as_view(), name="county_edit"),

    # Infrastructure
    path('infra/', InfraListView.as_view(), name="infra_list"),
    path('infra/add/', InfraCreateView.as_view(), name="infra_add"),
    path('infra/<int:pk>/edit/', InfraUpdateView.as_view(), name="infra_edit"),

    # Agriculture
    path('agri/', AgriListView.as_view(), name="agri_list"),
    path('agri/add/', AgriCreateView.as_view(), name="agri_add"),
    path('agri/<int:pk>/edit/', AgriUpdateView.as_view(), name="agri_edit"),

    # Economy
    path('economy/', EconomyListView.as_view(), name="economy_list"),
    path('economy/add/', EconomyCreateView.as_view(), name="economy_add"),
    path('economy/<int:pk>/edit/', EconomyUpdateView.as_view(), name="economy_edit"),

    # Demographics
    path('demo/', DemoListView.as_view(), name="demo_list"),
    path('demo/add/', DemoCreateView.as_view(), name="demo_add"),
    path('demo/<int:pk>/edit/', DemoUpdateView.as_view(), name="demo_edit"),

    # SQL Console
    path("sql/", sql_console, name="sql_console"),

    # Smart Query（大模型）
    path("smart/", smart_query, name="smart_query"),
    
    # Database Info
    path("database/", database_info, name="database_info"),
    
    # AI Prompt
    path("prompt/", view_prompt, name="view_prompt"),
    path("prompt/edit/", edit_prompt, name="edit_prompt"),

    # Auth login/logout/register
    path("login/", user_login, name="login"),
    path("register/", user_register, name="register"),
    path("logout/", user_logout, name="logout"),
    
    # User profile
    path("profile/", user_profile, name="user_profile"),
    path("profile/change_role/", change_role, name="change_role"),
    
    # Admin management (使用 manage/ 前缀避免与 Django admin 冲突)
    path("manage/users/", user_management, name="user_management"),
    path("manage/users/<int:user_id>/change_role/", change_user_role, name="change_user_role"),
    path("manage/users/<int:user_id>/toggle_admin/", toggle_admin, name="toggle_admin"),
    path("manage/users/<int:user_id>/table_permissions/", set_user_table_permissions, name="set_user_table_permissions"),
    path("manage/users/<int:user_id>/delete/", delete_user, name="delete_user"),
]
