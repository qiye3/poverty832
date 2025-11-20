from django.db import models


class County(models.Model):
    county_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=100, null=True, blank=True)   # ← 新增字段

    class Meta:
        unique_together = ('name', 'province')

    def __str__(self):
        return f"{self.name}（{self.city or self.province}）"


class InfrastructureService(models.Model):
    infra_id = models.AutoField(primary_key=True)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()

    pct_village_with_hard_road = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    pct_village_with_electricity = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    broadband_coverage = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    water_supply_coverage = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    sanitation_coverage = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.county.name} 基础设施 {self.year}"


class AgricultureSales(models.Model):
    sale_id = models.AutoField(primary_key=True)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()

    product_type = models.CharField(max_length=100, null=True)
    sales_volume = models.DecimalField(max_digits=18, decimal_places=2, null=True)
    sales_value = models.DecimalField(max_digits=18, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.county.name} 农业销售 {self.year}"


class CountyEconomy(models.Model):
    econ_id = models.AutoField(primary_key=True)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()

    gdp_total = models.DecimalField(max_digits=18, decimal_places=2, null=True)
    fiscal_revenue = models.DecimalField(max_digits=18, decimal_places=2, null=True)
    per_capita_income = models.DecimalField(max_digits=18, decimal_places=2, null=True)

    class Meta:
        unique_together = ('county', 'year')

    def __str__(self):
        return f"{self.county.name} 经济指标 {self.year}"


class CountyDemographics(models.Model):
    demo_id = models.AutoField(primary_key=True)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()

    population_total = models.BigIntegerField(null=True)
    urbanization_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    unemployment_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    migrant_workers = models.BigIntegerField(null=True)
    social_security_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.county.name} 人口结构 {self.year}"
