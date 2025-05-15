import os
from dotenv import load_dotenv
from langchain_core.tools import tool
import requests
import json


# 加载 .env 文件中的环境变量
load_dotenv(dotenv_path='D:/02File/05练习项目/04llm_learning/KEYs.env', override=True)


weather_api_key = os.environ["WEATHER_API_KEY"]

def city_code_search(city_name: str) -> str:
    """
    输入城市名称，返回城市代码。
    """
    # 打开并读取JSON文件
    with open('month1/week1/langgraph/tools/city_code.json', 'r', encoding='utf-8') as file:
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
            print(data)
            # print(f"API Response Data: {data}")
            tq = data['data']['tq']
            qw = data['data']['qw']
            return f"查询城市当前天气{tq}，气温{qw}度。"
        else:
            print(f"Error: {response.status_code}")   
    else:
        return "不支持查询该城市的天气"
    
print(search.invoke("北京"))