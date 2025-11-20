from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

from core.models import (
    County,
    InfrastructureService,
    AgricultureSales,
    CountyEconomy,
    CountyDemographics,
)


# ========= 通用 Mixin：为模板提供 model_name ========= #
class ModelNameMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 模型名称（避免 __name__）
        context["model_name"] = (
            self.model._meta.verbose_name or self.model.__name__
        )

        # 字段名列表（避免模板使用 _meta）
        context["field_names"] = [
            field.verbose_name or field.name
            for field in self.model._meta.fields
        ]

        # 字段属性名（用于取值）
        context["field_accessors"] = [
            field.name for field in self.model._meta.fields
        ]

        return context



# ==================== County ==================== #
class CountyListView(ModelNameMixin, ListView):
    model = County
    template_name = "core/generic_list.html"


class CountyCreateView(ModelNameMixin, CreateView):
    model = County
    fields = "__all__"
    template_name = "core/generic_form.html"
    success_url = reverse_lazy("county_list")


class CountyUpdateView(ModelNameMixin, UpdateView):
    model = County
    fields = "__all__"
    template_name = "core/generic_form.html"
    success_url = reverse_lazy("county_list")


# ================= Infrastructure ================= #
class InfraListView(ModelNameMixin, ListView):
    model = InfrastructureService
    template_name = "core/generic_list.html"


class InfraCreateView(ModelNameMixin, CreateView):
    model = InfrastructureService
    fields = "__all__"
    template_name = "core/generic_form.html"
    success_url = reverse_lazy("infra_list")


class InfraUpdateView(ModelNameMixin, UpdateView):
    model = InfrastructureService
    fields = "__all__"
    template_name = "core/generic_form.html"
    success_url = reverse_lazy("infra_list")


# ================= Agriculture ================= #
class AgriListView(ModelNameMixin, ListView):
    model = AgricultureSales
    template_name = "core/generic_list.html"


class AgriCreateView(ModelNameMixin, CreateView):
    model = AgricultureSales
    fields = "__all__"
    template_name = "core/generic_form.html"
    success_url = reverse_lazy("agri_list")


class AgriUpdateView(ModelNameMixin, UpdateView):
    model = AgricultureSales
    fields = "__all__"
    template_name = "core/generic_form.html"
    success_url = reverse_lazy("agri_list")


# ================= Economy ================= #
class EconomyListView(ModelNameMixin, ListView):
    model = CountyEconomy
    template_name = "core/generic_list.html"


class EconomyCreateView(ModelNameMixin, CreateView):
    model = CountyEconomy
    fields = "__all__"
    template_name = "core/generic_form.html"
    success_url = reverse_lazy("economy_list")


class EconomyUpdateView(ModelNameMixin, UpdateView):
    model = CountyEconomy
    fields = "__all__"
    template_name = "core/generic_form.html"
    success_url = reverse_lazy("economy_list")


# ================= Demographics ================= #
class DemoListView(ModelNameMixin, ListView):
    model = CountyDemographics
    template_name = "core/generic_list.html"


class DemoCreateView(ModelNameMixin, CreateView):
    model = CountyDemographics
    fields = "__all__"
    template_name = "core/generic_form.html"
    success_url = reverse_lazy("demo_list")


class DemoUpdateView(ModelNameMixin, UpdateView):
    model = CountyDemographics
    fields = "__all__"
    template_name = "core/generic_form.html"
    success_url = reverse_lazy("demo_list")
