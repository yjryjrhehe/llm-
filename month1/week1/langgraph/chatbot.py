import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatZhipuAI
import streamlit as st
from langchain.prompts import ChatPromptTemplate


from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# 加载 .env 文件中的环境变量
load_dotenv(dotenv_path='KEYs.env', override=True)
# 获取 API 密钥
llm_api_key = os.environ["ZHIPUAI_API_KEY"] 

llm = ChatZhipuAI(
    model="GLM-4-Air",
    api_key=llm_api_key,
    temperature=0
)



class State(TypedDict):
    # 定义一个状态字典，包含messages键，其类型为Annotated[list, add_messages]。
    # list 表示 messages 键的值应该是一个列表。
    # add_messages 是一个函数，它在 Annotated 注解中使用，
    # 提供了关于如何更新状态字典中 messages 的额外信息。
    # 这意味着 messages 键的值将是一个列表，并且在使用时会应用 add_messages 函数。
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

# 编译之后可以直接调用invoke函数来执行图。
# res = graph.invoke({"messages": [("user", '你好，从现在开始你叫aka'), ("ai", '你好呀！，我是aka。'),("user", '你叫什么名字？')]})
# print(res)

# state = State(messages = [("user", '你好，从现在开始你叫aka'), ("ai", '你好呀！，我是aka。'),("user", '你叫什么名字？')])
# # print(state)
# state["messages"] = add_messages(state["messages"], [("ai", '我叫aka'), ("user", '你叫什么名字？')])
# print("state:", state)
# res = graph.invoke(state)
# print("res:", res) # 这里res是一个字典，结构与state相同

# 直接获取到回复的答案，不包含中间过程。
# graph.invoke({"messages": [("user", '你是干什么的？')]})['messages'][-1].content

# state = State(messages=[("user", '你是干什么的？')])
# print("first state:", state)
# res = graph.invoke(state)['messages'][-1].content
# print("first result:",res)

# # 将机器人回复添加到对话历史
# state["messages"] = add_messages(state["messages"], [("ai", res)])
# print("second state:",state)
# [HumanMessage(content='你是干什么的？', additional_kwargs={}, response_metadata={}, id='6d88b34e-2d04-44a4-ac4b-46375a9679b5'), 
# AIMessage(content='我是一个人工智能助手，我的任务是针对用户的问题和要求提供适当的答复和支持。
# 我会根据你的问题 提供信息、解答疑问或者执行其他任务。有什么我可以帮助你的吗？', 
# additional_kwargs={}, response_metadata={}, id='91b17bb5-0f21-41ad-a223-4f644bfcaf38')]

#普通调用方法
def graph_updates(state: State):
    res = graph.invoke(state)
    print("Assistant:", res['messages'][-1].content)
    return res

state = State(messages=[])
while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    # 将用户输入添加到状态中
    state["messages"] = add_messages(state["messages"], [("user", user_input)])
    res = graph_updates(state)
    # 更新状态
    state = res


# # 流式调用方法
# def stream_graph_updates(state: State):
#     # graph.stream返回一个生成器对象，其中是每次更新后的状态
#     for event in graph.stream(state):
#         print("Current state:", state)
#         print("Event:", event)
#         for value in event.values():
#             print("Assistant:", value["messages"][-1].content)
#             return value["messages"][-1].content
#         # print(event.values())

# state = State(messages=[])
# while True:
#     user_input = input("User: ")
#     if user_input.lower() in ["quit", "exit", "q"]:
#         print("Goodbye!")
#         break
#     # 将用户输入添加到状态中
#     state["messages"] = add_messages(state["messages"], [("user", user_input)])

#     res = stream_graph_updates(state)
#     # 将机器人回复添加到状态中
#     state["messages"] = add_messages(state["messages"], [("ai", res)])
