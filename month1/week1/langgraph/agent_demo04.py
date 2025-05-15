import os
from dotenv import load_dotenv
from typing import Literal
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_community.chat_models import ChatZhipuAI
# pip install langgraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
import requests
import json
from tools.tools import search


# 加载 .env 文件中的环境变量
load_dotenv(dotenv_path='KEYs.env', override=True)
# 获取 API 密钥
llm_api_key = os.environ["ZHIPUAI_API_KEY"] 
tavily_api_key = os.environ["TAVILY_API_KEY"]

llm = ChatZhipuAI(
    model="GLM-4-Air",
    api_key=llm_api_key,
    temperature=0
)

# 定义工具函数，用于代理调用外部工具
from langchain_community.tools.tavily_search import TavilySearchResults
# 创建TavilySearchResults工具，设置最大结果数为1
tools = [TavilySearchResults(max_results=1, tavily_api_key=tavily_api_key), search]

from langchain import hub
import asyncio
from langgraph.prebuilt import create_react_agent

# 从LangChain的Hub中获取prompt模板，可以进行修改
# prompt = hub.pull("wfh/react-agent-executor")
# prompt.pretty_print()

# 创建一个REACT代理执行器，使用指定的LLM和工具，并应用从Hub中获取的prompt
agent_executor = create_react_agent(llm, tools)

# 调用代理执行器，询问“谁是美国公开赛的冠军”
# res = agent_executor.invoke({"messages": [("user", "谁是美国公开赛的获胜者")]})
res = agent_executor.invoke({"messages": [("user", "北京天气怎么样")]})
print(res)