import pandas as pd
from core.models import (
    County, InfrastructureService, AgricultureSales,
    CountyEconomy, CountyDemographics
)


# =============================
# 1. County 表
# =============================
def load_county():
    print("Loading County ...")
    df = pd.read_csv("data/county_202511201906.csv")

    for _, row in df.iterrows():
        County.objects.update_or_create(
            county_id=row["county_id"],
            defaults={
                "name": row["name"],
                "province": row["province"],
                "city": row["city"],  # ← 加到这里
            }
        )

    print(f"County 导入完成，共 {len(df)} 条记录.")



# =============================
# 2. InfrastructureService 表
# =============================
def load_infra():
    print("Loading InfrastructureService ...")
    df = pd.read_csv("data/infrastructureservice_202511201905.csv")

    for _, row in df.iterrows():
        # 对应外键 County
        county = County.objects.get(county_id=row["county_id"])

        InfrastructureService.objects.update_or_create(
            county=county,
            year=row["year"],
            defaults={
                "pct_village_with_hard_road": row.get("pct_village_with_hard_road"),
                "pct_village_with_electricity": row.get("pct_village_with_electricity"),
                "broadband_coverage": row.get("broadband_coverage"),
                "water_supply_coverage": row.get("water_supply_coverage"),
                "sanitation_coverage": row.get("sanitation_coverage"),
            }
        )
    print(f"InfrastructureService 导入完成，共 {len(df)} 条记录.")



# =============================
# 3. AgricultureSales 表
# =============================
def load_agri():
    print("Loading AgricultureSales ...")
    df = pd.read_csv("data/agriculturesales_202511201906.csv")

    for _, row in df.iterrows():
        county = County.objects.get(county_id=row["county_id"])

        AgricultureSales.objects.update_or_create(
            county=county,
            year=row["year"],
            product_type=row.get("product_type"),
            defaults={
                "sales_volume": row.get("sales_volume"),
                "sales_value": row.get("sales_value"),
            }
        )
    print(f"AgricultureSales 导入完成，共 {len(df)} 条记录.")



# =============================
# 4. CountyEconomy 表
# =============================
def load_economy():
    print("Loading CountyEconomy ...")
    df = pd.read_csv("data/countyeconomy_202511201906.csv")

    for _, row in df.iterrows():
        county = County.objects.get(county_id=row["county_id"])

        CountyEconomy.objects.update_or_create(
            county=county,
            year=row["year"],
            defaults={
                "gdp_total": row.get("gdp_total"),
                "fiscal_revenue": row.get("fiscal_revenue"),
                "per_capita_income": row.get("per_capita_income"),
            }
        )
    print(f"CountyEconomy 导入完成，共 {len(df)} 条记录.")



# =============================
# 5. CountyDemographics 表
# =============================
def load_demo():
    print("Loading CountyDemographics ...")
    df = pd.read_csv("data/countydemographics_202511201906.csv")

    for _, row in df.iterrows():
        county = County.objects.get(county_id=row["county_id"])

        CountyDemographics.objects.update_or_create(
            county=county,
            year=row["year"],
            defaults={
                "population_total": row.get("population_total"),
                "urbanization_rate": row.get("urbanization_rate"),
                "unemployment_rate": row.get("unemployment_rate"),
                "migrant_workers": row.get("migrant_workers"),
                "social_security_rate": row.get("social_security_rate"),
            }
        )
    print(f"CountyDemographics 导入完成，共 {len(df)} 条记录.")



# =============================
# 主入口：一键导入全部表
# =============================
def load_all():
    load_county()
    load_infra()
    load_agri()
    load_economy()
    load_demo()
    print("\n🎉 所有表已成功导入！")


# =============================
# 支持直接执行 load_data.py
# =============================
if __name__ == "__main__":
    load_all()
