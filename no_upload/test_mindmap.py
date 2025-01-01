import os
import dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentType
from xmind_tool import MindMapTool

# 加载环境变量
dotenv.load_dotenv()

def create_mindmap_agent():
    """创建思维导图生成代理"""
    # 初始化工具
    tools = [MindMapTool()]

    # 初始化语言模型
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-4o"
    )

    # 创建提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个专业的思维导图生成专家。你的任务是分析用户的自然语言描述，生成详细的多层次思维导图结构。

        思维导图生成规则：
        1. 主题分析：
           - 全面分析主题的各个维度和层面
           - 确保覆盖用户提供的所有关键点
           - 补充相关的重要方面
        
        2. 层次结构：
           - 第一层：核心主题
           - 第二层：主要维度（5-7个）
           - 第三层：具体分析点（每个维度3-5个）
           - 第四层：实施建议或具体案例（可选）
        
        3. 内容要求：
           - 逻辑性：确保各层次之间逻辑关系清晰
           - 完整性：每个维度都要有充分的展开和说明
           - 实用性：提供具体、可操作的内容
           - 前瞻性：包含未来趋势和发展方向
        
        4. 输出格式：
           - 使用MindMapTool生成多种格式文件
           - 支持FreeMind、OPML、XMind和MindManager格式
           - 确保文件结构完整，便于软件打开
        
        处理流程：
        1. 分析用户输入，提取核心主题和关键点
        2. 构建完整的思维导图层次结构
        3. 使用工具生成多格式文件
        4. 返回生成结果和文件路径
        
        注意事项：
        - 确保生成的思维导图既有广度又有深度
        - 内容要专业、准确、实用
        - 结构要清晰、合理、易于理解
        - 适应不同主题的特点，灵活调整结构"""),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # 创建代理
    agent = create_openai_functions_agent(llm, tools, prompt)
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )

def test_2025_business_opportunities():
    """测试用例1：2025创业机遇分析"""
    agent = create_mindmap_agent()
    input_data = """请为我分析2025年的创业机遇，需要考虑以下方面：
    1. 新兴技术领域的发展和机会
       - AI和机器学习的应用场景
       - 区块链和Web3的发展方向
       - 量子计算的商业化前景
       - 生物科技的突破点

    2. 社会需求和人口变化带来的机遇
       - 老龄化社会的服务需求
       - 新一代消费群体的特点
       - 远程办公和数字化生活
       - 教育和终身学习需求

    3. 政策支持和产业转型方向
       - 国家重点扶持领域
       - 传统产业数字化转型
       - 新基建带来的机会
       - 产业链重构趋势

    4. 全球化趋势和国际市场机会
       - 跨境电商和数字贸易
       - 新兴市场发展机遇
       - 全球供应链变革
       - 国际化人才服务

    5. 可持续发展和环保相关机遇
       - 清洁能源技术
       - 碳中和相关产业
       - 循环经济模式
       - 绿色消费趋势

    请深入分析每个方面，并提供具体的创业方向和机会点。"""
    
    return agent.invoke({"input": input_data})

def test_programming_languages():
    """测试用例2：编程语言对比分析"""
    agent = create_mindmap_agent()
    input_data = """请对主流编程语言进行深入对比分析，需要考虑以下方面：
    1. 各语言的核心特点和适用场景
       - Python：数据科学和AI
       - Java：企业级应用
       - JavaScript：前端和全栈
       - Go：云原生和微服务
       - Rust：系统编程和WebAssembly

    2. 性能和效率对比
       - 执行速度
       - 内存使用
       - 并发处理
       - 编译/解释特点

    3. 生态系统和社区支持
       - 包管理和库
       - 框架支持
       - 社区活跃度
       - 文档质量

    4. 学习曲线和开发效率
       - 语法复杂度
       - 开发工具支持
       - 调试便利性
       - 代码可维护性

    5. 就业市场需求和薪资水平
       - 岗位数量
       - 薪资范围
       - 区域分布
       - 经验要求

    6. 未来发展趋势和潜力
       - 技术演进方向
       - 新应用领域
       - 市场占有率变化
       - 企业采用意愿

    请提供详细的比较信息，帮助开发者选择适合的编程语言。"""
    
    return agent.invoke({"input": input_data})

def test_healthy_lifestyle():
    """测试用例3：个人健康生活指南"""
    agent = create_mindmap_agent()
    input_data = """请创建一个全面的个人健康生活指南，需要涵盖以下方面：
    1. 科学饮食和营养均衡
       - 膳食指南和营养素搭配
       - 食材选择和烹饪方法
       - 饮食习惯和进食时间
       - 特殊人群的营养需求

    2. 运动健身计划和方法
       - 有氧运动指南
       - 力量训练方案
       - 柔韧性和平衡训练
       - 运动强度和频率建议

    3. 心理健康和压力管理
       - 情绪识别和调节
       - 压力源识别和应对
       - 冥想和放松技巧
       - 社交关系维护

    4. 作息规律和睡眠质量
       - 科学作息时间
       - 睡眠环境优化
       - 入睡技巧和方法
       - 睡眠质量监测

    5. 环境因素和生活习惯
       - 室内空气质量
       - 光照和噪音管理
       - 个人卫生习惯
       - 环境整理和收纳

    6. 定期体检和健康监测
       - 体检项目和周期
       - 健康指标监测
       - 疾病预防措施
       - 医疗资源利用

    7. 职业健康和工作环境
       - 工作姿势和人体工程学
       - 办公环境改善
       - 工作压力管理
       - 职业病预防

    请为每个方面提供具体的建议和实施方案，帮助人们建立健康的生活方式。"""
    
    return agent.invoke({"input": input_data})

if __name__ == "__main__":
    print("测试用例1：2025创业机遇分析")
    result1 = test_2025_business_opportunities()
    print("\n" + "="*50 + "\n")

    print("测试用例2：编程语言对比分析")
    result2 = test_programming_languages()
    print("\n" + "="*50 + "\n")

    print("测试用例3：个人健康生活指南")
    result3 = test_healthy_lifestyle()
