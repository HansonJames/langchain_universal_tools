<div align="center">

<img src="https://raw.githubusercontent.com/langchain-ai/langchain/master/docs/static/img/langchain_banner.png" alt="LangChain Tools Banner" width="600px">

# 🛠️ LangChain Tools Collection

**Building a suite of powerful AI-powered tools with LangChain**

[English](README.md) | [简体中文](README_zh.md)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.3.13-green?logo=chainlink)](https://langchain.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange?logo=openai)](https://openai.com)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](https://opensource.org/licenses/Apache-2.0)

</div>

## 📬 Universal Email Assistant

Langchain has an official Gmail tool, but due to its complexity, I have developed a universal smart email tool that allows you to use natural language commands to send, read, and summarize emails.

### ✨ Features

- 🤖 Natural language interface for email management
- 🧠 AI-powered understanding and response
- 🚀 Multiple email provider support (QQ, 163, Aliyun)
- 📊 Smart email categorization and summarization

### 🚀 Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and configure your settings:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key and email settings
```

3. Use in your code:
```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from universal_email_tool import UniversalEmailTool, UniversalEmailToolReading

# Initialize tools and model
tools = [UniversalEmailTool(), UniversalEmailToolReading()]
llm = ChatOpenAI(temperature=0, model_name="gpt-4o")

# Create agent
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that processes email requests, read and summarize emails."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Example Features
# 1. Send a simple email
agent_executor.invoke({
    "input": "Send an email thanking John for the meeting"
})

# 2. Send HTML email with CC
agent_executor.invoke({
    "input": "Send HTML email to john@example.com, CC to team@example.com, with title 'Project Update'"
})

# 3. Send email with attachment
agent_executor.invoke({
    "input": "Send an email to john@example.com with the report.pdf attachment"
})

# 4. Read and summarize recent emails
agent_executor.invoke({
    "input": "Read and summarize my last 3 emails"
})

# 5. Categorize emails
agent_executor.invoke({
    "input": "Show my last 30 emails and categorize them"
})
```

## 🗺️ Roadmap

### Current Tools
- 📬 Universal Email Assistant
  - Email management through natural language
  - Multi-provider support
  - Smart summarization

### Upcoming Tools
- 📊 Data Analysis Assistant
  - Natural language data querying
  - Automated visualization
  - Insight generation

- 📝 Document Processing Tool
  - Multi-format document handling
  - Smart content extraction
  - Automated summarization

- 💬 Chat Interface Builder
  - Custom chatbot creation
  - Multi-platform deployment
  - Conversation flow design

- 🔍 Research Assistant
  - Literature review automation
  - Citation management
  - Research summarization

### Future Vision
- Building a comprehensive suite of AI-powered tools
- Creating seamless integrations between tools
- Developing a unified interface for all tools
- Supporting enterprise-level applications

## 🤝 Contributing

Contributions are welcome! Check out our [Contributing Guide](CONTRIBUTING.md) for more information.

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
