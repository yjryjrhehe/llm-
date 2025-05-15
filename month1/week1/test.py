import re

# def extract(text):
#     if "最终回复" in text:
#         response = text.split("最终回复", 1)[-1].strip()  # 使用 strip() 去除多余的空格和换行
#     else:
#         response = None  # 如果没有找到 "###Response"
#     return response

# text = """
# 制定回复策略

# 解释[\boxed{}]的来源和用途。
# 确认其在对话中的作用，增强用户理解。
# 鼓励用户继续提问，以满足其信息需求。
# 生成回复内容

# 使用清晰的语言解释[\boxed{}]的含义。
# 说明其在回复中的应用目的。
# 提供进一步的帮助和支持。
# 最终回复

# [\boxed{你好👋！欢迎再次与我交流！关于你提到的[\boxed{}]，这是一个数学公式排版中常用的标记，用于将内容框起来，使其突出显示。在我们的对话中，我使用[\boxed{}]来强调我的最终回复，使它更易于识别和阅读。希望这能帮助你理解我的回复结构！有什么其他问题或需要进一步解释的地方，随时告诉我哦！}]
# """

# # 使用正则表达式查找所有 "boxed" 标记内的内容
# pattern = r'$\boxed\{(.*?)\}$'
# matches = re.findall(pattern, text, re.DOTALL)

# # 输出找到的所有匹配项
# for i, match in enumerate(matches):
#     print(f"匹配 {i+1}: {match.strip()}")

# print(extract(text))

import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatZhipuAI
import streamlit as st
from langchain.prompts import ChatPromptTemplate

# # 加载 .env 文件中的环境变量
# load_dotenv(dotenv_path='ZHIPUAI_API_KEY.env', override=True)
# # 获取 API 密钥
# api_key = os.environ["ZHIPUAI_API_KEY"] 

# llm = ChatZhipuAI(
#     model="GLM-4-Air",
#     api_key=api_key,
#     temperature=0
# )

# res = llm.invoke("写一段使用python画心形的代码")
# print(res)