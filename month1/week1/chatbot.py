import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatZhipuAI
import streamlit as st
from langchain.prompts import ChatPromptTemplate

# 加载 .env 文件中的环境变量
load_dotenv(dotenv_path='KEYs.env', override=True)
# 获取 API 密钥
llm_api_key = os.environ["ZHIPUAI_API_KEY"] 

llm = ChatZhipuAI(
    model="GLM-4-Air",
    api_key=llm_api_key,
    temperature=0
)


# 定义提示词模板
template = """
你是一个智能助手，能够根据你与用户的对话历史和用户的最新问题生成你的回复。

以下是你和用户的对话历史：
{history}

用户的最新问题是：
{user_input}

请根据对话历史和最新问题生成你的回复。
"""

prompt = ChatPromptTemplate.from_template(template)

# 定义对话链
conversation = prompt | llm

st.set_page_config(page_title="对话机器人", page_icon="📖")
st.title("📖对话机器人📖")

# 初始化会话状态中的对话历史
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# 显示对话历史
for message in st.session_state.conversation_history:
    with st.chat_message("user" if message[0] == "human" else "AI"):
        st.markdown(message[1])

# 接收用户输入
if p_y :=st.chat_input("请输入您的问题："):
    # 将用户输入添加到对话历史
    st.session_state.conversation_history.append(("human", p_y))

    # 显示用户输入
    st.chat_message("user").markdown(p_y)

    # 调用模型生成回复
    res=conversation.invoke({"history": st.session_state.conversation_history, "user_input": p_y}).content

    # 将机器人回复添加到对话历史
    st.session_state.conversation_history.append(("ai", res))

    # 显示机器人回复
    st.chat_message("AI").markdown(res)

print(st.session_state.conversation_history)

