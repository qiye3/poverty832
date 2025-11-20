from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

from django.db.models import Avg, Sum

from core.models import (
    County, InfrastructureService, AgricultureSales,
    CountyEconomy, CountyDemographics
)
from core.forms import (
    CountyForm, InfraForm, AgriForm,
    EconomyForm, DemoForm
)


# ---------------------------
# 统计函数：根据模型自动生成统计卡片
# ---------------------------

def stats_for_model(model):
    """根据不同模型生成统计卡片"""

    if model == County:
        return [
            {"label": "县域数量", "value": model.objects.count()},
            {"label": "省份数量", "value": model.objects.values("province").distinct().count()},
        ]

    elif model == CountyEconomy:
        qs = model.objects
        return [
            {"label": "平均 GDP（亿元）", "value": round(qs.aggregate(Avg("gdp_total"))["gdp_total__avg"] or 0, 2)},
            {"label": "平均财政收入（亿元）", "value": round(qs.aggregate(Avg("fiscal_revenue"))["fiscal_revenue__avg"] or 0, 2)},
            {"label": "平均人均收入（元）", "value": round(qs.aggregate(Avg("per_capita_income"))["per_capita_income__avg"] or 0, 2)},
        ]

    elif model == InfrastructureService:
        qs = model.objects
        return [
            {"label": "平均硬化路覆盖率", "value": round(qs.aggregate(Avg("pct_village_with_hard_road"))["pct_village_with_hard_road__avg"] or 0, 2)},
            {"label": "平均宽带覆盖率", "value": round(qs.aggregate(Avg("broadband_coverage"))["broadband_coverage__avg"] or 0, 2)},
        ]

    elif model == CountyDemographics:
        qs = model.objects
        return [
            {"label": "总人口数", "value": qs.aggregate(Sum("population_total"))["population_total__sum"] or 0},
            {"label": "平均城镇化率", "value": round(qs.aggregate(Avg("urbanization_rate"))["urbanization_rate__avg"] or 0, 2)},
        ]

    elif model == AgricultureSales:
        qs = model.objects
        return [
            {"label": "总销售额（亿元）", "value": round(qs.aggregate(Sum("sales_value"))["sales_value__sum"] or 0, 2)},
        ]

    return []


# ---------------------------
# 通用列表视图（带统计 + 动态字段）
# ---------------------------

class GenericListView(ListView):
    template_name = "core/generic_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model = self.model

        # 自动表头：排除主键字段
        headers = [
            field.name
            for field in model._meta.fields
            if field.name != model._meta.pk.name
        ]

        context.update({
            "model_name": model.__name__,
            "headers": headers,
            "stats": stats_for_model(model),
        })
        return context


# ---------------------------
# 通用新增视图
# ---------------------------

class GenericCreateView(CreateView):
    template_name = "core/generic_form.html"

    def get_success_url(self):
        return reverse_lazy(f"{self.model.__name__.lower()}_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy(f"{self.model.__name__.lower()}_list")
        context['model_name'] = self.model.__name__
        return context


# ---------------------------
# 通用编辑视图
# ---------------------------

class GenericUpdateView(UpdateView):
    template_name = "core/generic_form.html"

    def get_success_url(self):
        return reverse_lazy(f"{self.model.__name__.lower()}_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy(f"{self.model.__name__.lower()}_list")
        context['model_name'] = self.model.__name__
        return context


# ---------------------------
# 以下是五张表的具体派生视图
# ---------------------------

# --- County ---
class CountyListView(GenericListView):
    model = County

class CountyCreateView(GenericCreateView):
    model = County
    form_class = CountyForm

class CountyUpdateView(GenericUpdateView):
    model = County
    form_class = CountyForm


# --- InfrastructureService ---
class InfraListView(GenericListView):
    model = InfrastructureService

class InfraCreateView(GenericCreateView):
    model = InfrastructureService
    form_class = InfraForm

class InfraUpdateView(GenericUpdateView):
    model = InfrastructureService
    form_class = InfraForm


# --- AgricultureSales ---
class AgriListView(GenericListView):
    model = AgricultureSales

class AgriCreateView(GenericCreateView):
    model = AgricultureSales
    form_class = AgriForm

class AgriUpdateView(GenericUpdateView):
    model = AgricultureSales
    form_class = AgriForm


# --- CountyEconomy ---
class EconomyListView(GenericListView):
    model = CountyEconomy

class EconomyCreateView(GenericCreateView):
    model = CountyEconomy
    form_class = EconomyForm

class EconomyUpdateView(GenericUpdateView):
    model = CountyEconomy
    form_class = EconomyForm


# --- CountyDemographics ---
class DemoListView(GenericListView):
    model = CountyDemographics

class DemoCreateView(GenericCreateView):
    model = CountyDemographics
    form_class = DemoForm

class DemoUpdateView(GenericUpdateView):
    model = CountyDemographics
    form_class = DemoForm
