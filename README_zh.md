<div align="center">

<img src="https://raw.githubusercontent.com/langchain-ai/langchain/master/docs/static/img/langchain_banner.png" alt="LangChain Tools Banner" width="600px">

# 🛠️ LangChain 工具集

**使用 LangChain 构建强大的 AI 驱动工具套件**

[English](README.md) | [简体中文](README_zh.md)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.3.13-green?logo=chainlink)](https://langchain.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange?logo=openai)](https://openai.com)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](https://opensource.org/licenses/Apache-2.0)

</div>

## 📬 通用邮件助手

langchain官方有一个gmail邮箱工具，但是因为操作起来很复杂，所以本人开发了一个通用智能邮箱工具，允许您使用自然语言命令发送、阅读和总结邮件等。

### ✨ 特性

- 🤖 自然语言邮件管理界面
- 🧠 AI驱动的理解和响应
- 🚀 多邮件服务商支持（QQ、163、阿里云）
- 📊 智能邮件分类和总结

### 🚀 快速开始

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 复制 `.env.example` 到 `.env` 并配置：
```bash
cp .env.example .env
# 编辑 .env 文件，设置 OpenAI API 密钥和邮箱配置
```

3. 在代码中使用：
```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from universal_email_tool import UniversalEmailTool, UniversalEmailToolReading

# 初始化工具和模型
tools = [UniversalEmailTool(), UniversalEmailToolReading()]
llm = ChatOpenAI(temperature=0, model_name="gpt-4o")

# 创建代理
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that processes email requests, read and summarize emails."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 功能示例
# 1. 发送简单邮件
agent_executor.invoke({
    "input": "发封邮件感谢张三参加会议"
})

# 2. 发送带抄送的HTML邮件
agent_executor.invoke({
    "input": "发送HTML邮件到zhang@example.com，抄送到team@example.com，标题为'项目更新'"
})

# 3. 发送带附件的邮件
agent_executor.invoke({
    "input": "给zhang@example.com发送一封邮件，附上report.pdf文件"
})

# 4. 读取并总结邮件
agent_executor.invoke({
    "input": "读取并总结我最近的3封邮件"
})

# 5. 邮件分类
agent_executor.invoke({
    "input": "显示我最近30封邮件并进行分类"
})
```

## 🗺️ 发展规划

### 当前工具
- 📬 通用邮件助手
  - 自然语言邮件管理
  - 多服务商支持
  - 智能总结功能

### 即将推出
- 📊 数据分析助手
  - 自然语言数据查询
  - 自动化可视化
  - 洞察生成

- 📝 文档处理工具
  - 多格式文档处理
  - 智能内容提取
  - 自动化总结

- 💬 聊天界面构建器
  - 自定义聊天机器人创建
  - 多平台部署
  - 对话流程设计

- 🔍 研究助手
  - 文献综述自动化
  - 引用管理
  - 研究总结

### 未来愿景
- 构建全面的AI驱动工具套件
- 创建工具间的无缝集成
- 开发统一的工具界面
- 支持企业级应用

## 🤝 贡献

欢迎贡献！查看我们的[贡献指南](CONTRIBUTING.md)了解更多信息。

## 📄 许可证

本项目采用 Apache License 2.0 许可证 - 详见 [LICENSE](LICENSE) 文件。
