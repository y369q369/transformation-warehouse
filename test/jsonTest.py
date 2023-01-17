import json

# 读取json文件
with open("jsonFile.json", 'r', encoding='utf-8') as load_f:
    load_dict = json.load(load_f)
    print(load_dict)
