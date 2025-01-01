from langchain.tools import BaseTool
import xml.etree.ElementTree as ET
import xml.dom.minidom
from typing import List, Dict, Union
import os
import zipfile
import json
import uuid
import time
from langchain_community.utilities import SerpAPIWrapper
from pydantic import Field
from langchain_openai import ChatOpenAI


class UniversalMindMapTool(BaseTool):
    """用于生成思维导图的通用工具"""

    name: str = "mindmap_generator"
    description: str = "用于生成思维导图的工具。输入主题，自动生成多种格式的思维导图文件。"
    search: SerpAPIWrapper = Field(default_factory=SerpAPIWrapper)
    output_dir: str = Field(default="output/mindmap")
    llm: ChatOpenAI = Field(default_factory=lambda: ChatOpenAI(temperature=0, model_name="gpt-4o"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        os.makedirs(self.output_dir, exist_ok=True)

    def _search_and_analyze(self, topic: str, requirements: str = None) -> Dict:
        """搜索和分析主题相关信息"""
        # 使用搜索工具获取主题相关信息
        search_result = self.search.run(f"{topic} 主要方面 分析")

        # 使用LLM分析搜索结果并生成思维导图结构
        prompt = f"""
        请根据以下信息，生成一个关于"{topic}"的思维导图结构。

        搜索结果：
        {search_result}

        要求：
        1. 生成5-7个主要方面
        2. 每个方面包含3-5个具体的子主题
        3. 每个子主题可以包含2-3个关键点
        4. 结构要清晰，内容要专业准确
        5. 输出格式为JSON，示例：
        {{
            "main_topic": "主题",
            "subtopics": [
                {{
                    "name": "主要方面1",
                    "subtopics": [
                        {{
                            "name": "子主题1",
                            "subtopics": ["关键点1", "关键点2"]
                        }}
                    ]
                }}
            ]
        }}
        """

        response = self.llm.invoke(prompt)
        try:
            # 提取JSON部分
            start = response.content.find('{')
            end = response.content.rfind('}') + 1
            mindmap_data = json.loads(response.content[start:end])
        except Exception as e:
            print(f"JSON解析错误: {str(e)}")
            # 返回基本结构
            mindmap_data = {
                "main_topic": topic,
                "subtopics": []
            }

        return mindmap_data

    def _generate_freemind(self, main_topic: str, subtopics: List, output_dir: str) -> str:
        """生成FreeMind格式思维导图文件"""
        root = ET.Element("map", version="1.0.1")
        center_node = ET.SubElement(root, "node", TEXT=main_topic)

        def add_subtopics(parent_node, topics):
            if not topics:
                return
            for topic in topics:
                if isinstance(topic, dict):
                    child = ET.SubElement(parent_node, "node", TEXT=topic.get('name', ''))
                    if 'subtopics' in topic:
                        add_subtopics(child, topic['subtopics'])
                else:
                    ET.SubElement(parent_node, "node", TEXT=str(topic))

        add_subtopics(center_node, subtopics)

        file_path = os.path.join(output_dir, f"{main_topic}.mm")
        xmlstr = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(xmlstr)

        return file_path

    def _generate_opml(self, main_topic: str, subtopics: List, output_dir: str) -> str:
        """生成OPML格式思维导图文件"""
        root = ET.Element("opml", version="2.0")
        head = ET.SubElement(root, "head")
        title = ET.SubElement(head, "title")
        title.text = main_topic
        body = ET.SubElement(root, "body")
        center_outline = ET.SubElement(body, "outline", text=main_topic)

        def add_subtopics(parent_node, topics):
            if not topics:
                return
            for topic in topics:
                if isinstance(topic, dict):
                    child = ET.SubElement(parent_node, "outline", text=topic.get('name', ''))
                    if 'subtopics' in topic:
                        add_subtopics(child, topic['subtopics'])
                else:
                    ET.SubElement(parent_node, "outline", text=str(topic))

        add_subtopics(center_outline, subtopics)

        file_path = os.path.join(output_dir, f"{main_topic}.opml")
        xmlstr = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(xmlstr)

        return file_path

    def _generate_xmind(self, main_topic: str, subtopics: List, output_dir: str) -> str:
        """生成XMind格式思维导图文件"""
        temp_dir = os.path.join(output_dir, "temp_xmind")
        os.makedirs(temp_dir, exist_ok=True)

        def create_topic_structure(topic_data):
            if isinstance(topic_data, str):
                return {
                    "id": str(uuid.uuid4()),
                    "class": "topic",
                    "title": topic_data
                }
            elif isinstance(topic_data, dict):
                topic = {
                    "id": str(uuid.uuid4()),
                    "class": "topic",
                    "title": topic_data.get('name', '')
                }
                if 'subtopics' in topic_data and topic_data['subtopics']:
                    topic["children"] = {
                        "attached": [create_topic_structure(sub) for sub in topic_data['subtopics']]
                    }
                return topic
            return None

        content = {
            "id": str(uuid.uuid4()),
            "class": "sheet",
            "title": "Sheet 1",
            "rootTopic": create_topic_structure({
                "name": main_topic,
                "subtopics": subtopics
            })
        }

        content_json = json.dumps([content], indent=2)
        with open(os.path.join(temp_dir, "content.json"), "w", encoding="utf-8") as f:
            f.write(content_json)

        metadata = {
            "creator": {
                "name": "XMind",
                "version": "23.07.100148"
            },
            "timestamp": int(time.time() * 1000),
            "version": "2.0"
        }

        metadata_json = json.dumps(metadata, indent=2)
        with open(os.path.join(temp_dir, "metadata.json"), "w", encoding="utf-8") as f:
            f.write(metadata_json)

        manifest = {
            "file-entries": {
                "content.json": {},
                "metadata.json": {},
                "Thumbnails/thumbnail.png": {}
            }
        }

        manifest_json = json.dumps(manifest, indent=2)
        with open(os.path.join(temp_dir, "manifest.json"), "w", encoding="utf-8") as f:
            f.write(manifest_json)

        thumbnails_dir = os.path.join(temp_dir, "Thumbnails")
        os.makedirs(thumbnails_dir, exist_ok=True)
        with open(os.path.join(thumbnails_dir, "thumbnail.png"), "wb") as f:
            f.write(b"")

        file_path = os.path.join(output_dir, f"{main_topic}.xmind")
        with zipfile.ZipFile(file_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    file_path_in_zip = os.path.relpath(os.path.join(root, file), temp_dir)
                    zf.write(os.path.join(root, file), file_path_in_zip)

        import shutil
        shutil.rmtree(temp_dir)

        return file_path

    def _generate_mindmanager(self, main_topic: str, subtopics: List, output_dir: str) -> str:
        """生成MindManager格式思维导图文件"""
        root = ET.Element("map", version="1.0")
        root.set("xmlns:ap", "http://schemas.mindjet.com/MindManager/Application/2003")
        root.set("xmlns", "http://schemas.mindjet.com/MindManager/Map/2003")

        center_node = ET.SubElement(root, "topic")
        text = ET.SubElement(center_node, "text")
        text.text = main_topic

        def add_subtopics(parent_node, topics):
            if not topics:
                return
            for topic in topics:
                topic_node = ET.SubElement(parent_node, "topic")
                text_node = ET.SubElement(topic_node, "text")
                if isinstance(topic, dict):
                    text_node.text = topic.get('name', '')
                    if 'subtopics' in topic:
                        add_subtopics(topic_node, topic['subtopics'])
                else:
                    text_node.text = str(topic)

        add_subtopics(center_node, subtopics)

        file_path = os.path.join(output_dir, f"{main_topic}.mmap")
        xmlstr = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(xmlstr)

        return file_path

    def _run(self, topic: str, requirements: str = None) -> Dict[str, str]:
        """生成思维导图

        Args:
            topic: 主题
            requirements: 具体要求（可选）

        Returns:
            包含不同格式文件路径的字典
        """
        # 搜索和分析数据
        mindmap_data = self._search_and_analyze(topic, requirements)

        # 生成不同格式的文件
        mm_path = self._generate_freemind(mindmap_data["main_topic"], mindmap_data["subtopics"], self.output_dir)
        opml_path = self._generate_opml(mindmap_data["main_topic"], mindmap_data["subtopics"], self.output_dir)
        xmind_path = self._generate_xmind(mindmap_data["main_topic"], mindmap_data["subtopics"], self.output_dir)
        mmap_path = self._generate_mindmanager(mindmap_data["main_topic"], mindmap_data["subtopics"], self.output_dir)

        return {
            "freemind": mm_path,
            "opml": opml_path,
            "xmind": xmind_path,
            "mindmanager": mmap_path
        }

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError("不支持异步操作")


class UniversalMindMapToolReading(BaseTool):
    """用于读取和分析思维导图的工具"""

    name: str = "mindmap_reader"
    description: str = "用于读取和分析思维导图文件。输入文件路径，输出思维导图的结构化内容。"

    def _run(self, file_path: str) -> Dict:
        """读取思维导图文件

        Args:
            file_path: 思维导图文件路径

        Returns:
            思维导图的结构化内容
        """
        # TODO: 实现思维导图读取功能
        raise NotImplementedError("思维导图读取功能尚未实现")

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError("不支持异步操作")
