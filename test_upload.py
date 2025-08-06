import requests
import json

# 测试上传压缩包
url = "http://localhost:8000/api/v1/files/upload-and-extract"

# 准备文件
files = {
    'file': ('test_project.zip', open('test_project.zip', 'rb'), 'application/zip')
}

try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print("Upload successful!")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"Upload failed with status {response.status_code}")
        
except Exception as e:
    print(f"Error: {e}")
finally:
    files['file'][1].close()
