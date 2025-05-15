#示例：langgraph_hello.py
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


# 加载 .env 文件中的环境变量
load_dotenv(dotenv_path='KEYs.env', override=True)
# 获取 API 密钥
llm_api_key = os.environ["ZHIPUAI_API_KEY"] 

llm = ChatZhipuAI(
    model="GLM-4-Air",
    api_key=llm_api_key,
    temperature=0
)

weather_api_key = os.environ["WEATHER_API_KEY"]

def city_code_search(city_name: str) -> str:
    """
    输入城市名称，返回城市代码。
    """
    # 打开并读取JSON文件
    with open('month1/week1/langgraph/city_code.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    # 访问数据
    for province in data['list']:
        for city in province['list']:
            if city['name'] == city_name:
                return city['city_id']
    return None
# 定义工具函数，用于代理调用外部工具
@tool
def search(city_name: str) -> str:
    """
    输入城市名称，获取天气信息。
    """
    city_code = city_code_search(city_name)
    if city_code:
        # API 地址
        url = "http://api.yytianqi.com/observe"
        # 可选的查询参数
        params = {
            "city": city_code,
            "key": weather_api_key
        }
        # 发送 GET 请求
        response = requests.get(url, params=params)
        # 检查响应状态码
        if response.status_code == 200:
            # 解析返回的数据（假设是 JSON 格式）
            data = response.json()
            # print(f"API Response Data: {data}")
            tq = data['data']['tq']
            qw = data['data']['qw']
            return f"查询城市当前天气{tq}，气温{qw}度。"
        else:
            print(f"Error: {response.status_code}")   
    else:
        return "不支持查询该城市的天气"

# 将工具函数放入工具列表
tools = [search]

# 创建工具节点
tool_node = ToolNode(tools)

# 1.初始化模型和工具，定义并绑定工具到模型
model = llm.bind_tools(tools)

# 定义函数，决定是否继续执行
def should_continue(state: MessagesState) -> Literal["tools", END]: # type: ignore
    messages = state['messages']
    last_message = messages[-1]
    # 如果LLM调用了工具，则转到“tools”节点
    if last_message.tool_calls:
        return "tools"
    # 否则，停止（回复用户）
    return END


# 定义调用模型的函数
def call_model(state: MessagesState):
    messages = state['messages']
    response = model.invoke(messages)
    # 返回列表，因为这将被添加到现有列表中
    return {"messages": [response]}

# 2.用状态初始化图，定义一个新的状态图
workflow = StateGraph(MessagesState)
# 3.定义图节点，定义我们将循环的两个节点
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# 4.定义入口点和图边
# 设置入口点为“agent”
# 这意味着这是第一个被调用的节点
workflow.set_entry_point("agent")

# 添加条件边
workflow.add_conditional_edges(
    # 首先，定义起始节点。我们使用`agent`。
    # 这意味着这些边是在调用`agent`节点后采取的。
    "agent",
    # 接下来，传递决定下一个调用节点的函数。
    should_continue,
)

# 添加从`tools`到`agent`的普通边。
# 这意味着在调用`tools`后，接下来调用`agent`节点。
workflow.add_edge("tools", 'agent')

# 初始化内存以在图运行之间持久化状态
checkpointer = MemorySaver()

# 5.编译图
# 这将其编译成一个LangChain可运行对象，
# 这意味着你可以像使用其他可运行对象一样使用它。
# 注意，我们（可选地）在编译图时传递内存
app = workflow.compile(checkpointer=checkpointer)
# app = workflow.compile()

# 6.执行图，使用可运行对象
final_state = app.invoke(
    # {"messages": [HumanMessage(content="北京（城市代码为CH010100）和上海（城市代码为CH020100）的天气怎么样?")]},
    {"messages": [HumanMessage(content="北京的天气怎么样?")]},
    # {"messages": [HumanMessage(content="北京的城市代码是多少?")]},
    config={"configurable": {"thread_id": 42}}
)
# 从 final_state 中获取最后一条消息的内容
result = final_state["messages"][-1].content
print(result)
print(final_state)
final_state = app.invoke(
    {"messages": [HumanMessage(content="我问的哪个城市?")]},
    config={"configurable": {"thread_id": 42}}
)
result = final_state["messages"][-1].content
print(result)
print(final_state)