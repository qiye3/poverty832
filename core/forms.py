from django import forms
from .models import (
    County, InfrastructureService, AgricultureSales,
    CountyEconomy, CountyDemographics
)


class CountyForm(forms.ModelForm):
    class Meta:
        model = County
        fields = "__all__"


class InfrastructureServiceForm(forms.ModelForm):
    class Meta:
        model = InfrastructureService
        fields = "__all__"


class AgricultureSalesForm(forms.ModelForm):
    class Meta:
        model = AgricultureSales
        fields = "__all__"


class CountyEconomyForm(forms.ModelForm):
    class Meta:
        model = CountyEconomy
        fields = "__all__"


class CountyDemographicsForm(forms.ModelForm):
    class Meta:
        model = CountyDemographics
        fields = "__all__"
