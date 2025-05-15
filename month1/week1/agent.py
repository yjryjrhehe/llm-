import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatZhipuAI
import streamlit as st
from langchain.prompts import ChatPromptTemplate
import requests
from langchain.agents import initialize_agent
from langchain.agents import AgentType
# 导入tool函数装饰器
from langchain.agents import tool

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
# print(weather_api_key)

from pydantic import BaseModel, Field
from langchain.tools import StructuredTool


class WeatherInput(BaseModel):
    city_code: str = Field(description="城市代码，必须是一个字符串。")
@tool
def weather(city_code: str) -> str:
    """
    输入城市代码，获取天气信息。
    """

    # API 地址
    url = "http://api.yytianqi.com/observe"

    # 可选的查询参数
    params = {
        "city": city_code,
        "key": weather_api_key
    }
    print(city_code)
    print(f"Constructed URL: {url}?city={city_code}&key={weather_api_key}")  # 打印构造的 URL
    # 发送 GET 请求
    response = requests.get(url, params=params)
    print(response.url)

    # 检查响应状态码
    if response.status_code == 200:
        # 解析返回的数据（假设是 JSON 格式）
        data = response.json()
        print(f"API Response Data: {data}")
        return f"查询结果：{data}",data
    else:
        print(f"Error: {response.status_code}")   


weather_search = StructuredTool.from_function(
    func=weather,
    name="weather_search",
    description="输入城市代码，获取天气信息。",
    args_schema=WeatherInput,
    return_direct=True,
    handle_tool_error=True,
)

# 初始化代理，并传递工具列表
agent = initialize_agent(
    tools=[weather_search], 
    llm=llm, 
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, 
    verbose=True
    )

# print(agent)
# 使用代理进行查询
response = agent.invoke("查询北京的天气，城市代码为CH010100")
print(response)  # 输出天气信息

res, data = weather.invoke("CH010100")
print(data['data']['tq'])

# llm_with_tools = llm.bind_tools(tools=[weather])
# res = llm_with_tools.invoke("今天北京天气怎么样？北京的城市代码为CH010100")
# print(res)

# agent= initialize_agent(
#     tools=[weather], #将刚刚创建的工具加入代理
#     llm=llm, #初始化的模型
#     agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,  #代理类型
#     handle_parsing_errors=True, #处理解析错误
#     verbose = True #输出中间步骤
# )


# res = agent.run("今天北京天气怎么样？北京的城市代码为101010100")

# print(res)