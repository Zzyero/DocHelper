import requests
import json
import time

def test_complete_flow():
    """测试完整的文件上传到报告生成流程"""
    
    # 步骤1: 上传并解压文件
    print("步骤1: 上传并解压文件...")
    try:
        with open('test_project.zip', 'rb') as f:
            files = {'file': ('test_project.zip', f, 'application/zip')}
            response = requests.post('http://localhost:8000/api/v1/files/upload-and-extract', files=files)
            
        if response.status_code != 200:
            print(f"上传失败: {response.status_code}")
            print(response.text)
            return False
            
        upload_result = response.json()
        print(f"✅ 上传成功: {upload_result['count']} 个文件")
        extracted_files = upload_result['extracted_files']
        
    except Exception as e:
        print(f"❌ 上传失败: {e}")
        return False
    
    # 步骤2: 创建项目
    print("\n步骤2: 创建项目...")
    try:
        file_paths = [f['path'] for f in extracted_files]
        data = {
            'name': '测试项目',
            'description': '用于测试的项目',
            'file_paths': file_paths
        }
        
        response = requests.post('http://localhost:8000/api/v1/projects', data=data)
        
        if response.status_code != 200:
            print(f"创建项目失败: {response.status_code}")
            print(response.text)
            return False
            
        project_result = response.json()
        project_id = project_result['project']['id']
        print(f"✅ 项目创建成功: {project_id}")
        
    except Exception as e:
        print(f"❌ 创建项目失败: {e}")
        return False
    
    # 步骤3: 生成报告
    print("\n步骤3: 生成报告...")
    try:
        data = {
            'project_id': project_id,
            'format_type': 'markdown',
            'custom_prompt': '请生成一个简单的实验报告'
        }
        
        response = requests.post('http://localhost:8000/api/v1/generate', data=data)
        
        if response.status_code != 200:
            print(f"生成报告失败: {response.status_code}")
            print(response.text)
            return False
            
        generate_result = response.json()
        print(f"✅ 报告生成成功!")
        print(f"   输出路径: {generate_result['output_path']}")
        print(f"   报告长度: {len(generate_result['report_content'])} 字符")
        
        # 保存报告到文件
        with open(f"test_report_{int(time.time())}.md", "w", encoding="utf-8") as f:
            f.write(generate_result['report_content'])
        print("   报告已保存到本地文件")
        
        return True
        
    except Exception as e:
        print(f"❌ 生成报告失败: {e}")
        return False

if __name__ == "__main__":
    print("开始测试完整的文件上传到报告生成流程...")
    print("=" * 50)
    
    success = test_complete_flow()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 所有测试通过！完整的流程工作正常。")
    else:
        print("💥 测试失败！请检查错误信息。")
