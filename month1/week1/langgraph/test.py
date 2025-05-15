import json
# from agent_demo03 import city_code_search

# 打开并读取JSON文件
with open('month1/week1/langgraph/city_code.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 访问数据
print(data['list'][13]['list'][2]['name'])
for province in data['list']:
    for city in province['list']:
        if city['name'] == '北京':
            print(city['city_id'])

def city_code_search(city_name: str) -> str:
    """
    输入城市名称，返回城市代码。
    """
    # 打开并读取JSON文件
    with open('month1/week1/langgraph/city_code.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    # 访问数据
    print(data['list'][13]['list'][2]['name'])
    for province in data['list']:
        for city in province['list']:
            if city['name'] == city_name:
                return city['city_id']
    return "没有找到该城市"

print(city_code_search('wo'))
