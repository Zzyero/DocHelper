import requests
import json

# 测试报告生成
url = "http://localhost:8000/api/v1/generate"

# 使用刚才创建的项目ID
project_id = "proj_1754460461555"

# 准备数据
data = {
    "project_id": project_id,
    "format_type": "markdown",
    "custom_prompt": "请基于上传的JavaScript代码和README文件生成一个简单的实验报告"
}

try:
    response = requests.post(url, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print("Report generation successful!")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"Report generation failed with status {response.status_code}")
        
except Exception as e:
    print(f"Error: {e}")
