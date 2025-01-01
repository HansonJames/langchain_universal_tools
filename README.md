# Universal LangChain Tools

A collection of universal tools based on LangChain for various tasks.

[中文文档](README_zh.md)

## Features

### 1. Universal Email Tool
- Send emails with various formats (plain text, HTML)
- Support attachments
- Read and summarize emails
- Multiple email service providers support (QQ, 163, Aliyun)

### 2. Universal Mind Map Tool
- Generate mind maps from any topic automatically
- Support multiple mind map formats (FreeMind, OPML, XMind, MindManager)
- Intelligent content analysis and organization
- Easy to use with simple API

## Installation

```bash
git clone https://github.com/HansonJames/langchain_universal_tools.git
cd langchain_universal_tools
pip install -r requirements.txt
```

## Configuration

Create a `.env` file with the following content:

```env
# OpenAI and SerpAPI settings
OPENAI_API_KEY=your_openai_api_key
SERPAPI_API_KEY=your_serpapi_api_key

# Email service settings
EMAIL_USE=QQ  # QQ, 163, or ALIYUN
EMAIL_CONFIGS={
    "QQ": {
        "smtp_host": "smtp.qq.com",
        "smtp_port": 465,
        "imap_host": "imap.qq.com",
        "username": "your_qq_email",
        "password": "your_email_password"
    }
}
```

## Usage

### Email Tool

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from universal_email_tool import UniversalEmailTool, UniversalEmailToolReading

# Initialize tools
tools = [UniversalEmailTool(), UniversalEmailToolReading()]

# Initialize the language model
llm = ChatOpenAI(
    temperature=0,
    model_name="gpt-4o"
)

# Create the agent
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Send email
result = agent_executor.invoke({
    "input": "Send an email to example@qq.com with subject 'Test' and content 'Hello'"
})

# Read emails
result = agent_executor.invoke({
    "input": "Read and summarize my recent 3 emails"
})
```

### Mind Map Tool

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from xmind_tool import UniversalMindMapTool, UniversalMindMapToolReading

# Initialize tools
tools = [UniversalMindMapTool(), UniversalMindMapToolReading()]

# Initialize the language model
llm = ChatOpenAI(
    temperature=0,
    model_name="gpt-4o"
)

# Create the agent
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Generate mind map
topic = "Programming Languages Comparison"
result = agent_executor.invoke({
    "input": f"Please generate a mind map about '{topic}'."
})
```

## Output Formats

### Email Tool
- Plain text emails
- HTML formatted emails
- Support for attachments
- Email reading and summarization

### Mind Map Tool
- FreeMind (.mm)
- OPML (.opml)
- XMind (.xmind)
- MindManager (.mmap)

All mind map files are saved in the `output/mindmap` directory.

## Requirements

- Python 3.8+
- OpenAI API key
- SerpAPI key (for mind map generation)
- Email service account
- Required Python packages (see requirements.txt)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
