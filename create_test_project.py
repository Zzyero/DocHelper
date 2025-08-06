import requests
import json

# 创建测试项目
url = "http://localhost:8000/api/v1/projects"

# 准备数据
data = {
    "name": "Test Project",
    "description": "A test project for DocHelper",
    "file_paths": [
        "uploads/extracted/test_project/README.md",
        "uploads/extracted/test_project/test.js"
    ]
}

try:
    response = requests.post(url, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print("Project creation successful!")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"Project creation failed with status {response.status_code}")
        
except Exception as e:
    print(f"Error: {e}")
