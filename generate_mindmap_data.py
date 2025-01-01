import os
import json
import dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentType
from langchain_community.utilities import SerpAPIWrapper
from langchain.tools import Tool
from xmind_tool import MindMapTool

# 加载环境变量
dotenv.load_dotenv()

def create_research_agent():
    """创建研究代理，用于收集和分析数据"""
    # 初始化搜索工具
    search = SerpAPIWrapper()
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="用于搜索特定主题的最新信息和趋势。输入应该是一个搜索查询。"
        )
    ]

    # 初始化语言模型
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-4o"
    )

    # 创建提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个专业的研究分析师。你需要使用搜索工具收集信息，并将结果整理成结构化的JSON格式。

输出格式示例：
{{
    "main_topic": "主题名称",
    "subtopics": [
        {{
            "name": "子主题1",
            "subtopics": [
                {{
                    "name": "子主题1.1",
                    "subtopics": ["要点1", "要点2"]
                }}
            ]
        }}
    ]
}}

要求：
1. 信息要准确、及时
2. 结构要清晰、层次分明
3. 内容要有深度和广度
4. 包含具体的例子和数据"""),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # 创建代理
    agent = create_openai_functions_agent(llm, tools, prompt)
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True
    )

def create_mindmap_agent():
    """创建思维导图生成代理"""
    tools = [MindMapTool()]
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-4o"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个专业的思维导图生成专家。你需要将JSON格式的数据转换为思维导图。

处理规则：
1. 分析输入的JSON数据结构
2. 确保主题层次清晰
3. 保持逻辑关系完整
4. 生成多种格式的思维导图文件

注意事项：
- 确保所有层级的主题都有明确的标题
- 内容要简洁但信息量充足
- 结构要清晰易懂
- 适应不同主题的特点"""),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_openai_functions_agent(llm, tools, prompt)
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True
    )

def generate_mindmap(topic: str, requirements: str = None):
    """生成思维导图
    
    Args:
        topic: 主题
        requirements: 具体要求（可选）
    """
    print(f"\n开始研究主题：{topic}")
    
    # 创建研究代理
    research_agent = create_research_agent()
    
    # 构建研究提示
    if requirements:
        research_prompt = f"请对'{topic}'进行深入研究，需要特别关注以下方面：{requirements}"
    else:
        research_prompt = f"请对'{topic}'进行全面深入的研究，收集最新信息和趋势。"
    
    print("\n正在收集和分析数据...")
    
    # 收集研究数据
    research_data = research_agent.invoke({"input": research_prompt})
    
    # 提取JSON数据
    try:
        # 在返回的文本中查找JSON结构
        start = research_data['output'].find('{')
        end = research_data['output'].rfind('}') + 1
        mindmap_data = json.loads(research_data['output'][start:end])
        print("\nJSON数据提取成功")
    except (json.JSONDecodeError, KeyError) as e:
        print(f"\nError: 无法从研究数据中提取JSON结构: {str(e)}")
        print("原始输出:", research_data['output'])
        return None
    
    print("\n开始生成思维导图...")
    
    # 创建思维导图生成代理
    mindmap_agent = create_mindmap_agent()
    
    # 生成思维导图
    result = mindmap_agent.invoke({
        "input": f"请根据以下数据生成思维导图：{json.dumps(mindmap_data, ensure_ascii=False, indent=2)}"
    })
    
    return result

if __name__ == "__main__":
    # 测试用例：未来智能家居发展趋势
    print("\n=== 测试用例：未来智能家居发展趋势 ===")
    result = generate_mindmap(
        "未来智能家居发展趋势",
        """
        1. 技术发展和创新
        2. 市场需求和用户体验
        3. 产业生态和标准化
        4. 安全和隐私保护
        5. 能源管理和可持续发展
        """
    )
    print("\n生成结果：")
    print(result)
