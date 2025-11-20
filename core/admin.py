from django.contrib import admin
from .models import (
    County, InfrastructureService, AgricultureSales,
    CountyEconomy, CountyDemographics, UserTablePermission, AIPromptConfig
)

admin.site.register(County)
admin.site.register(InfrastructureService)
admin.site.register(AgricultureSales)
admin.site.register(CountyEconomy)
admin.site.register(CountyDemographics)
admin.site.register(UserTablePermission)

@admin.register(AIPromptConfig)
class AIPromptConfigAdmin(admin.ModelAdmin):
    list_display = ['updated_at', 'updated_by']
    fields = ['table_schema', 'system_prompt', 'user_prompt_template']
    
    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
