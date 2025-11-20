import os
import openai
from django.conf import settings

openai.api_key = settings.DOUBAO_API_KEY
openai.api_base = "https://ark.cn-beijing.volces.com/api/v3"   # Doubao API

# 你项目中的所有表结构，让 AI 能理解数据库
TABLE_SCHEMA = """
你正在查询一个 SQLite 数据库，它包含以下数据表（注意使用 Django 默认命名）：

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
- 不要写分号之外的多条 SQL。
"""


def ask_doubao_sql(question: str):
    """向 Doubao 请求 SQL 生成 + 解释"""

    prompt = f"""
你是一个 SQL 助手，请严格根据下面的数据库结构为用户生成正确的 SQL。

{TABLE_SCHEMA}

用户的问题是：
【{question}】

请输出：
1. 一条可执行的 SQL 查询语句（只要 SQL，本行不要自然语言）
2. 对查询结果的自然语言解释（简短）

格式要求：

SQL:
<你的 SQL>

Explanation:
<自然语言说明>
"""

    response = openai.ChatCompletion.create(
        model="ep-20250118102936-tdz6m",  # Doubao-pro（示例 endpoint，请换成你的）
        messages=[
            {"role": "system", "content": "你是一个专业 SQL 帮助助手。"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    text = response["choices"][0]["message"]["content"]

    # 解析 SQL 和 Explanation
    sql = ""
    explanation = ""

    if "SQL:" in text:
        sql = text.split("SQL:")[1].split("Explanation:")[0].strip()

    if "Explanation:" in text:
        explanation = text.split("Explanation:")[1].strip()

    return sql, explanation

# ⚠ 注意：上面 endpoint 是示例（ep-20250118102936-tdz6m）
# 你需要替换成你在火山方舟控制台创建的模型 endpoint。