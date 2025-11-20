import os
from django.conf import settings

# 尝试导入新版本OpenAI（1.0+）
try:
    from openai import OpenAI
    OPENAI_NEW_VERSION = True
except ImportError:
    # 如果导入失败，尝试旧版本
    try:
        import openai
        OPENAI_NEW_VERSION = False
    except ImportError:
        OPENAI_NEW_VERSION = None

# ================================
# AI 配置
# ================================
# 支持的AI服务类型：'doubao', 'openai', 'custom'
AI_SERVICE_TYPE = getattr(settings, 'AI_SERVICE_TYPE', 'doubao')

# API配置（支持多种环境变量名）
AI_API_KEY = getattr(settings, 'AI_API_KEY', os.getenv('AI_API_KEY') or os.getenv('DOUBAO_API_KEY') or os.getenv('ARK_API_KEY'))
AI_API_BASE = getattr(settings, 'AI_API_BASE', None)  # 如果为None，使用默认值
AI_MODEL = getattr(settings, 'AI_MODEL', None)  # 如果为None，使用默认值

def get_ai_config():
    """获取AI配置"""
    service_type = AI_SERVICE_TYPE
    
    if service_type == 'doubao':
        # 豆包（火山方舟）配置
        api_base = AI_API_BASE or "https://ark.cn-beijing.volces.com/api/v3"
        model = AI_MODEL or "ep-20250118102936-tdz6m"  # ⚠️ 请替换为你在火山方舟控制台创建的endpoint ID
    elif service_type == 'openai':
        # OpenAI配置
        api_base = AI_API_BASE or "https://api.openai.com/v1"
        model = AI_MODEL or "gpt-3.5-turbo"
    elif service_type == 'custom':
        # 自定义AI服务（OpenAI兼容API）
        api_base = AI_API_BASE or "https://api.openai.com/v1"
        model = AI_MODEL or "gpt-3.5-turbo"
    else:
        # 默认使用豆包
        api_base = AI_API_BASE or "https://ark.cn-beijing.volces.com/api/v3"
        model = AI_MODEL or "ep-20250118102936-tdz6m"  # ⚠️ 请替换为你在火山方舟控制台创建的endpoint ID
    
    return {
        'api_key': AI_API_KEY,
        'api_base': api_base,
        'model': model
    }

def get_prompt_config():
    """从数据库获取prompt配置，如果不存在则使用默认值"""
    try:
        from core.models import AIPromptConfig
        config = AIPromptConfig.get_config()
        return {
            'table_schema': config.table_schema,
            'system_prompt': config.system_prompt,
            'user_prompt_template': config.user_prompt_template,
        }
    except Exception:
        # 如果数据库未迁移或出错，使用默认值
        return {
            'table_schema': """你正在查询一个 SQLite 数据库，它包含以下数据表（注意使用 Django 默认命名）：

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
- 不要写分号之外的多条 SQL。""",
            'system_prompt': "你是一个专业 SQL 帮助助手。",
            'user_prompt_template': """你是一个 SQL 助手，请严格根据下面的数据库结构为用户生成正确的 SQL。

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
        }


def ask_ai_sql(question: str):
    """
    向AI请求SQL生成 + 解释
    支持多种AI服务：Doubao、OpenAI、自定义OpenAI兼容API
    兼容OpenAI API 1.0+ 和旧版本
    """
    
    ai_config = get_ai_config()
    prompt_config = get_prompt_config()
    
    if not ai_config['api_key']:
        return "", "AI API密钥未配置，请在settings.py或环境变量中设置AI_API_KEY"

    # 使用数据库中的prompt模板
    user_prompt = prompt_config['user_prompt_template'].format(
        table_schema=prompt_config['table_schema'],
        question=question
    )

    try:
        # 根据OpenAI版本选择不同的调用方式
        if OPENAI_NEW_VERSION:
            # 新版本OpenAI API (1.0+)
            client = OpenAI(
                api_key=ai_config['api_key'],
                base_url=ai_config['api_base']
            )
            
            response = client.chat.completions.create(
                model=ai_config['model'],
                messages=[
                    {"role": "system", "content": prompt_config['system_prompt']},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
            )
            
            text = response.choices[0].message.content
        else:
            # 旧版本OpenAI API (<1.0)
            import openai
            openai.api_key = ai_config['api_key']
            openai.api_base = ai_config['api_base']
            
            response = openai.ChatCompletion.create(
                model=ai_config['model'],
                messages=[
                    {"role": "system", "content": prompt_config['system_prompt']},
                    {"role": "user", "content": user_prompt},
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
    
    except Exception as e:
        error_msg = str(e)
        # 提供更友好的错误提示
        if "InvalidEndpointOrModel" in error_msg or "404" in error_msg or "does not exist" in error_msg:
            return "", f"AI请求失败：模型或endpoint不存在。\n\n请检查：\n1. 在.env文件中设置正确的AI_MODEL（你的endpoint ID）\n2. 确认endpoint在火山方舟控制台中已创建并可用\n3. 检查API密钥是否有访问该endpoint的权限\n\n详细配置请参考：AI_CONFIG.md\n\n原始错误：{error_msg}"
        elif "401" in error_msg or "Unauthorized" in error_msg or "Invalid API key" in error_msg:
            return "", f"AI请求失败：API密钥无效或未授权。\n\n请检查：\n1. 在.env文件中设置正确的AI_API_KEY\n2. 确认API密钥是否有效\n3. 检查API密钥是否有足够的权限\n\n详细配置请参考：AI_CONFIG.md\n\n原始错误：{error_msg}"
        else:
            return "", f"AI请求失败：{error_msg}\n\n请检查API密钥和配置是否正确。详细配置请参考：AI_CONFIG.md"


def get_full_prompt(question: str):
    """获取完整的prompt内容（用于显示给用户）"""
    prompt_config = get_prompt_config()
    return {
        'system_prompt': prompt_config['system_prompt'],
        'user_prompt': prompt_config['user_prompt_template'].format(
            table_schema=prompt_config['table_schema'],
            question=question
        ),
        'table_schema': prompt_config['table_schema'],
    }


# 为了保持向后兼容，保留旧函数名
def ask_doubao_sql(question: str):
    """向后兼容的别名"""
    return ask_ai_sql(question)