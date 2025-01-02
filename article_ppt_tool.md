# 基于LangChain的通用PPT生成工具

一个基于LangChain和DALL-E的智能PPT生成工具，可以自动生成包含专业内容和精美配图的演示文稿。

项目地址：https://github.com/HansonJames/langchain_universal_tools

## 主要特点

1. 智能内容生成
   - 自动生成完整的PPT大纲
   - 基于最新数据的市场分析
   - 专业的内容组织和结构

2. 高质量配图
   - 使用DALL-E 3生成专业配图
   - 自动适配16:9幻灯片比例
   - 图文搭配合理

3. 数据支持
   - 实时搜索最新市场数据
   - 自动提取关键数据点
   - 数据可视化展示

4. 易用性
   - 简单的API接口
   - 自动保存为PPTX格式
   - 支持自定义页数和主题

## 使用示例

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import StructuredTool
from universal_ppt_tool import PPTGenerator

# 初始化工具
ppt_generator = PPTGenerator()
tools = [
    StructuredTool.from_function(
        func=ppt_generator.generate_with_logging,
        name="generate_ppt",
        description="生成PPT的工具",
    )
]

# 初始化语言模型
llm = ChatOpenAI(
    model_name="gpt-4o",
    temperature=0
)

# 创建代理
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 生成PPT
topic = "2025年的创业机遇"
result = agent_executor.invoke({
    "input": f"""请为我生成一个主题为"{topic}"的PPT，需要3页。要求：
    1. 内容要全面且具有前瞻性
    2. 包含最新的市场数据和趋势
    3. 重点分析未来的创业方向
    4. 配图要专业且美观
    """
})
```

## 技术特点

1. 基于LangChain的智能代理系统
2. 使用DALL-E 3生成高质量配图
3. 实时数据搜索和分析
4. 自动化的PPT生成流程
5. 结构化的内容组织

## 应用场景

- 市场分析报告
- 商业计划书
- 行业趋势分析
- 项目提案
- 教育培训材料

## 系统要求

- Python 3.8+
- OpenAI API密钥
- 所需Python包（见requirements.txt）

## 输出示例

生成的PPT包含：
- 专业的封面设计
- 结构化的内容页
- 数据支持的分析
- DALL-E生成的配图
- 清晰的总结展望

所有PPT文件都保存在`output/ppt`目录下。
