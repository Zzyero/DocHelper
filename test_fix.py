import requests
import json

def test_generate_with_dynamic_project():
    """测试使用动态项目ID的报告生成功能"""
    url = "http://localhost:8000/api/v1/generate"
    
    # 使用动态生成的项目ID
    import time
    project_id = f"proj_{int(time.time() * 1000)}"
    
    # 准备数据 - 使用实际存在的测试文件
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
            return True
        else:
            print(f"Report generation failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing report generation with dynamic project ID...")
    success = test_generate_with_dynamic_project()
    if success:
        print("✅ Test passed!")
    else:
        print("❌ Test failed!")
