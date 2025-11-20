from django.contrib import admin
from .models import (
    County, InfrastructureService, AgricultureSales,
    CountyEconomy, CountyDemographics
)

admin.site.register(County)
admin.site.register(InfrastructureService)
admin.site.register(AgricultureSales)
admin.site.register(CountyEconomy)
admin.site.register(CountyDemographics)
