import operator
from typing import Annotated, List, Tuple, TypedDict
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
import json



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


# 定义一个TypedDict类PlanExecute，用于存储输入、计划、过去的步骤和响应
class PlanExecute(TypedDict):
    input: str
    plan: List[str]
    past_steps: Annotated[List[Tuple], operator.add]
    response: str

from pydantic import BaseModel, Field


# 定义一个Plan模型类，用于描述未来要执行的计划
# class Plan(BaseModel):
#     """未来要执行的计划"""

#     steps: List[str] = Field(
#         description="需要执行的不同步骤，应该按顺序排列"
#     )

from langchain_core.prompts import ChatPromptTemplate

# 创建一个计划生成的提示模板
planner_prompt = ChatPromptTemplate.from_template("""
    你是一位高效的助手，擅长将复杂的任务分解为一系列简单、具体的步骤，以确保任务可以被准确无误地完成。
    请根据以下具体要求，为给定的目标或问题设计一个逐步计划，并将结果以JSON格式输出，注意结果中不要出现"json"等无关字符串：

    要求：
    - 你的回答应该直接针对上述目标，提出一个简明的逐步计划。
    - 每个步骤都应该是独立且必需的，如果按顺序正确执行这些步骤，将会得到正确的最终答案。
    - 避免添加任何不必要的步骤或额外解释。
    - 确保每一步骤都包含了所有必要的信息，不跳过任何关键细节。
    - 最后一个步骤应当能够直接获得最终的答案。

    根据以上要求，以下是基于示例目标的生成逐步计划：
    示例：
    “计算从2023年1月1日至2025年5月4日之间的总天数。”

    结果：
    ["确认起始日期为2023年1月1日，结束日期为2025年5月4日",
    "计算2023年的剩余天数（从1月1日起）",
    "加上2024年的全年天数（注意检查是否为闰年）",
    "加上2025年直到5月4日为止的天数",
    "将上述步骤中得到的所有天数加起来，得出总天数作为最终答案"]

    现在，请根据上述格式和要求，为以下目标制定一个逐步计划：
    {messages}
    """)


def parse_plan(plan: str) -> List[str]:
    """
    解析计划字符串，将其转换为列表。
    """
    # 使用json.loads将字符串转换为Python列表
    try:
        return json.loads(plan)
    except json.JSONDecodeError:
        # 如果解析失败，返回一个空列表
        return []

# 使用指定的提示模板创建一个计划生成器，使用OpenAI的ChatGPT-4o模型
# planner = planner_prompt | llm.with_structured_output(Plan, include_raw=True)
planner = planner_prompt | llm

# 调用计划生成器，询问“当前澳大利亚公开赛冠军的家乡是哪里？”
res = planner.invoke({"messages":"现任澳网冠军的家乡是哪里?"})

# 转换为 Python 列表
res_list = json.loads(res.content)

print(res_list)