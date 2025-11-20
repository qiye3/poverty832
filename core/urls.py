from django.urls import path
from django.contrib import admin   # ← 新增
from django.urls import include    # ← 新增

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
from core.views.auth import user_login, user_logout, user_register
from core.views.user_profile import user_profile, change_role


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

    # Auth login/logout/register
    path("login/", user_login, name="login"),
    path("register/", user_register, name="register"),
    path("logout/", user_logout, name="logout"),

    # Django Admin（可留可不留）
    path('admin/', admin.site.urls),
]
