from django.db import models
from django.contrib.auth.models import User


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


class UserTablePermission(models.Model):
    """用户对每张表的细粒度权限"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='table_permissions')
    table_name = models.CharField(max_length=50)  # 'county', 'infra', 'agri', 'economy', 'demo'
    can_view = models.BooleanField(default=True)
    can_edit = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'table_name')
        verbose_name = '用户表权限'
        verbose_name_plural = '用户表权限'
    
    def __str__(self):
        return f"{self.user.username} - {self.table_name} (view:{self.can_view}, edit:{self.can_edit})"


class AIPromptConfig(models.Model):
    """AI Prompt配置（单例模式）"""
    table_schema = models.TextField(help_text="数据库表结构说明，用于AI理解数据库")
    system_prompt = models.TextField(default="你是一个专业 SQL 帮助助手。", help_text="AI系统提示词")
    user_prompt_template = models.TextField(
        default="""你是一个 SQL 助手，请严格根据下面的数据库结构为用户生成正确的 SQL。

{table_schema}

用户的问题是：
【{question}】

请输出：
1. 一条可执行的 SQL 查询语句（只要 SQL，本行不要自然语言）
2. 对查询结果的自然语言解释（简短）

格式要求：

SQL:
<你的 SQL>

Explanation:
<自然语言说明>""",
        help_text="用户提示词模板，{table_schema}和{question}会被替换"
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='prompt_configs')
    
    class Meta:
        verbose_name = 'AI Prompt配置'
        verbose_name_plural = 'AI Prompt配置'
    
    def __str__(self):
        return f"AI Prompt配置 (更新于: {self.updated_at})"
    
    @classmethod
    def get_config(cls):
        """获取配置（单例模式）"""
        config = cls.objects.first()
        if not config:
            # 创建默认配置
            config = cls.objects.create(
                table_schema="""你正在查询一个 SQLite 数据库，它包含以下数据表（注意使用 Django 默认命名）：

1️⃣ core_county:
- county_id (int, PK)
- name (varchar)
- province (varchar)
- city (varchar, nullable)

2️⃣ core_infrastructureservice:
- infra_id (int, PK)
- county_id (FK → county)
- year (int)
- pct_village_with_hard_road
- pct_village_with_electricity
- broadband_coverage
- water_supply_coverage
- sanitation_coverage

3️⃣ core_agriculturesales:
- sale_id (int, PK)
- county_id
- year
- product_type
- sales_volume
- sales_value

4️⃣ core_countyeconomy:
- econ_id
- county_id
- year
- gdp_total
- fiscal_revenue
- per_capita_income

5️⃣ core_countydemographics:
- demo_id
- county_id
- year
- population_total
- urbanization_rate
- unemployment_rate
- migrant_workers
- social_security_rate

⚠ 注意：
- 所有表名必须使用 Django ORM 的真实表名，例如 core_county。
- SQLite 中不支持 ILIKE。
- 不要写分号之外的多条 SQL。"""
            )
        return config
