#!/usr/bin/env python3
"""
DocHelper 项目启动脚本
用于同时启动前端和后端服务
"""

import subprocess
import sys
import os
import time
from threading import Thread

def print_banner():
    """打印启动横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║   ██████╗  ██████╗██╗  ██╗███████╗██████╗ ██╗   ██╗████████╗ ║
    ║   ██╔══██╗██╔════╝██║  ██║██╔════╝██╔══██╗██║   ██║╚══██╔══╝ ║
    ║   ██║  ██║██║     ███████║█████╗  ██████╔╝██║   ██║   ██║    ║
    ║   ██║  ██║██║     ██╔══██║██╔══╝  ██╔══██╗██║   ██║   ██║    ║
    ║   ██████╔╝╚██████╗██║  ██║███████╗██║  ██║╚██████╔╝   ██║    ║
    ║   ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝    ║
    ║                                                              ║
    ║                实验报告自动生成工具                          ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def start_backend():
    """启动后端服务"""
    print("🚀 正在启动后端服务...")
    try:
        # 使用 uvicorn 启动后端服务
        backend_process = subprocess.Popen([
            sys.executable, "-c", 
            "import sys; sys.path.append('.'); from backend.main import app; import uvicorn; uvicorn.run('backend.main:app', host='127.0.0.1', port=8000, reload=True)"
        ], cwd=os.getcwd())
        print("✅ 后端服务启动成功!")
        print("   后端API地址: http://localhost:8000")
        print("   API文档: http://localhost:8000/docs")
        return backend_process
    except Exception as e:
        print(f"❌ 后端服务启动失败: {e}")
        return None

def start_frontend():
    """启动前端服务"""
    print("🚀 正在启动前端服务...")
    try:
        # 直接使用 node_modules 中的 vite
        vite_path = os.path.join(os.getcwd(), "node_modules", ".bin", "vite.cmd")
        if os.path.exists(vite_path):
            frontend_process = subprocess.Popen([vite_path], cwd=os.getcwd())
        else:
            # 备用方案：使用 npx
            frontend_process = subprocess.Popen(["npx", "vite"], cwd=os.getcwd())
        print("✅ 前端服务启动成功!")
        print("   前端页面地址: http://localhost:5173")
        return frontend_process
    except Exception as e:
        print(f"❌ 前端服务启动失败: {e}")
        return None

def main():
    """主函数"""
    print_banner()
    print("🔧 正在初始化 DocHelper 项目...")
    
    # 检查必要的文件和目录
    required_files = [
        "backend/main.py",
        "src/main.js",
        "package.json"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ 缺少必要文件: {file}")
            return
    
    # 启动后端服务
    backend_process = start_backend()
    if not backend_process:
        print("❌ 无法启动后端服务，程序退出")
        return
    
    # 等待后端服务启动
    print("⏳ 等待后端服务完全启动...")
    time.sleep(3)
    
    # 启动前端服务
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ 无法启动前端服务")
        backend_process.terminate()
        return
    
    print("\n🎉 DocHelper 项目启动完成!")
    print("\n📋 访问地址:")
    print("   🌐 前端页面: http://localhost:5173")
    print("   🔧 后端API: http://localhost:8000")
    print("   📚 API文档: http://localhost:8000/docs")
    print("   ❤️  健康检查: http://localhost:8000/health")
    
    print("\n💡 使用说明:")
    print("   1. 打开浏览器访问 http://localhost:5173")
    print("   2. 在'文件上传'页面上传您的项目文件")
    print("   3. 在'报告生成'页面生成实验报告")
    print("   4. 在'历史记录'页面下载生成的报告")
    
    print("\n⏹️  按 Ctrl+C 停止所有服务")
    
    try:
        # 等待任一进程结束
        while True:
            if backend_process.poll() is not None:
                print("❌ 后端服务已停止")
                frontend_process.terminate()
                break
            if frontend_process.poll() is not None:
                print("❌ 前端服务已停止")
                backend_process.terminate()
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 正在停止所有服务...")
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ 所有服务已停止")
        sys.exit(0)

if __name__ == "__main__":
    main()
