from django import forms
from .models import (
    County,
    InfrastructureService,
    AgricultureSales,
    CountyEconomy,
    CountyDemographics
)

# ------------------------------
# County
# ------------------------------
class CountyForm(forms.ModelForm):
    class Meta:
        model = County
        fields = "__all__"


# ------------------------------
# Infrastructure
# ------------------------------
class InfraForm(forms.ModelForm):
    class Meta:
        model = InfrastructureService
        fields = "__all__"


# ------------------------------
# Agriculture Sales
# ------------------------------
class AgriForm(forms.ModelForm):
    class Meta:
        model = AgricultureSales
        fields = "__all__"


# ------------------------------
# County Economy
# ------------------------------
class EconomyForm(forms.ModelForm):
    class Meta:
        model = CountyEconomy
        fields = "__all__"


# ------------------------------
# Demographics
# ------------------------------
class DemoForm(forms.ModelForm):
    class Meta:
        model = CountyDemographics
        fields = "__all__"
