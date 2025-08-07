@echo off
title DocHelper 启动器

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║   ██████╗  ██████╗██╗  ██╗███████╗██████╗ ██╗   ██╗████████╗ ║
echo ║   ██╔══██╗██╔════╝██║  ██║██╔════╝██╔══██╗██║   ██║╚══██╔══╝ ║
echo ║   ██║  ██║██║     ███████║█████╗  ██████╔╝██║   ██║   ██║    ║
echo ║   ██║  ██║██║     ██╔══██║██╔══╝  ██╔══██╗██║   ██║   ██║    ║
echo ║   ██████╔╝╚██████╗██║  ██║███████╗██║  ██║╚██████╔╝   ██║    ║
echo ║   ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝    ║
echo ║                                                              ║
echo ║                实验报告自动生成工具                          ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🚀 正在启动 DocHelper 项目...
echo.

echo 🔧 启动后端服务...
start "DocHelper Backend" /min python -c "import sys; sys.path.append('.'); from backend.main import app; import uvicorn; uvicorn.run('backend.main:app', host='127.0.0.1', port=8000, reload=True)"

echo ⏳ 等待后端服务启动...
timeout /t 5 /nobreak >nul

echo 🔧 启动前端服务...
start "DocHelper Frontend" /min cmd /c "npx vite && pause"

echo.
echo 🎉 启动完成!
echo.
echo 📋 访问地址:
echo    🌐 前端页面: http://localhost:5173
echo    🔧 后端API: http://localhost:8000
echo    📚 API文档: http://localhost:8000/docs
echo.
echo ⏳ 请稍等片刻，让服务完全启动...
echo.
echo 🛑 关闭此窗口将停止所有服务
echo.

pause
