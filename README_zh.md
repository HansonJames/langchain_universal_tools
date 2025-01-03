# 通用LangChain工具集

基于LangChain的通用工具集，用于各种任务。

## 功能特点

### 1. 通用邮件工具
- 支持多种格式邮件发送（纯文本、HTML）
- 支持附件功能
- 邮件阅读和摘要生成
- 支持多个邮件服务提供商（QQ、163、阿里云）

### 2. 通用思维导图工具
- 自动根据主题生成思维导图
- 支持多种思维导图格式（FreeMind、OPML、XMind、MindManager）
- 智能内容分析和组织
- 简单易用的API接口

### 3. 通用PPT工具
- 自动生成专业演示文稿
- DALL-E 3生成高质量配图
- 实时集成市场数据
- 专业的内容组织
- 支持自定义页数和主题

## 安装

```bash
git clone https://github.com/HansonJames/langchain_universal_tools.git
cd langchain_universal_tools
pip install -r requirements.txt
```

## 配置

创建`.env`文件，添加以下内容：

```env
# OpenAI和SerpAPI设置
OPENAI_API_KEY=你的OpenAI API密钥
SERPAPI_API_KEY=你的SerpAPI密钥

# 邮件服务设置
EMAIL_USE=QQ  # QQ、163或ALIYUN
EMAIL_CONFIGS={
    "QQ": {
        "smtp_host": "smtp.qq.com",
        "smtp_port": 465,
        "imap_host": "imap.qq.com",
        "username": "你的QQ邮箱",
        "password": "你的邮箱密码"
    }
}
```

## 使用方法

### 邮件工具

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from universal_email_tool import UniversalEmailTool, UniversalEmailToolReading

# 初始化工具
tools = [UniversalEmailTool(), UniversalEmailToolReading()]

# 初始化语言模型
llm = ChatOpenAI(
    temperature=0,
    model_name="gpt-4o"
)

# 创建代理
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 发送邮件
result = agent_executor.invoke({
    "input": "向example@qq.com发送一封主题为'测试'，内容为'你好'的邮件"
})

# 读取邮件
result = agent_executor.invoke({
    "input": "阅读并总结我最近的3封邮件"
})
```

### 思维导图工具

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from xmind_tool import UniversalMindMapTool, UniversalMindMapToolReading

# 初始化工具
tools = [UniversalMindMapTool(), UniversalMindMapToolReading()]

# 初始化语言模型
llm = ChatOpenAI(
    temperature=0,
    model_name="gpt-4o"
)

# 创建代理
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 生成思维导图
topic = "编程语言对比分析"
result = agent_executor.invoke({
    "input": f"请生成一个关于'{topic}'的思维导图。"
})
```

### PPT工具

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

## 输出格式

### 邮件工具
- 纯文本邮件
- HTML格式邮件
- 支持附件
- 邮件阅读和摘要

### 思维导图工具
- FreeMind格式 (.mm)
- OPML格式 (.opml)
- XMind格式 (.xmind)
- MindManager格式 (.mmap)

所有思维导图文件都保存在`output/mindmap`目录下。

### PPT工具
- PowerPoint格式 (.pptx)
- 专业的版式设计
- DALL-E生成的配图
- 数据驱动的内容

所有PPT文件都保存在`output/ppt`目录下。

## 系统要求

- Python 3.8+
- OpenAI API密钥
- SerpAPI密钥（用于思维导图生成）
- 邮件服务账号
- 所需Python包（见requirements.txt）

## 许可证

Apache 许可证

## 贡献

欢迎提交Pull Request！
