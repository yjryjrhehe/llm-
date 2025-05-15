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
from langchain_core.utils.function_calling import convert_to_openai_tool

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
    # print(city_code)
    # print(f"Constructed URL: {url}?city={city_code}&key={weather_api_key}")  # 打印构造的 URL
    # 发送 GET 请求
    response = requests.get(url, params=params)
    # print(response.url)

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

@tool
def sum_nums(s1: float, s2: float):
    """对给定输入的结果求和。"""
    return "结果是 {a}".format(a = s1+s2)

tools =[weather, sum_nums]
zhipu_tools = [convert_to_openai_tool(f) for f in tools]
llm_tools = llm.bind(tools=zhipu_tools)

res = llm_tools.invoke("查询北京的天气，城市代码为CH010100")
# print(res.tool_calls[0]["args"])

name = res.tool_calls[0]["name"]
args = res.tool_calls[0]["args"]


param = {
    "city_code": args["city_code"]
}
weather_res = weather.invoke(input=args)
print(weather_res)