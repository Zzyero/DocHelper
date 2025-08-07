# DocHelper 使用说明

## 🚀 启动服务

### 方法一：使用一键启动脚本（推荐）

**Windows用户:**
```bash
# 双击运行或在命令行执行
start_dev.bat
```

**PowerShell用户:**
```bash
# 在PowerShell中执行
powershell -ExecutionPolicy Bypass -File start_dev.ps1
```

### 方法二：手动启动

**1. 启动后端服务:**
```bash
# 在项目根目录执行
python -c "import sys; sys.path.append('.'); from backend.main import app; import uvicorn; uvicorn.run('backend.main:app', host='127.0.0.1', port=8000, reload=True)"
```

**2. 启动前端服务:**
```bash
# 在项目根目录执行
npm run dev
```

## 🌐 访问应用

服务启动后，打开浏览器访问：
- **主页面**: http://localhost:5173
- **API文档**: http://localhost:8000/docs

## 📝 使用流程

### 1. 文件上传
1. 访问 http://localhost:5173/#/upload
2. 点击"选择文件"或拖拽文件到上传区域
3. 支持的文件类型：`.py`, `.js`, `.java`, `.cpp`, `.md` 等
4. 点击"上传文件"按钮

### 2. 生成实验报告
1. 访问 http://localhost:5173/#/generate
2. 选择已上传的项目文件
3. 选择报告格式：
   - **Markdown** (.md) - 快速生成
   - **Word** (.docx) - 专业格式
4. 点击"生成报告"按钮
5. 等待AI分析和生成（约30秒-2分钟）

### 3. 查看和下载报告
1. 访问 http://localhost:5173/#/history
2. 查看生成的报告列表
3. 点击"下载"按钮保存报告

## 🤖 AI对话功能

1. 访问 http://localhost:5173/#/ai-chat
2. 输入技术问题或代码相关询问
3. AI助手将提供详细的解答和指导

## ⚙️ 系统设置

1. 访问 http://localhost:5173/#/settings
2. 配置AI服务参数
3. 设置默认报告模板
4. 管理输出目录

## 📊 报告生成功能

### 支持的格式
- **Markdown** (.md) - 轻量级标记语言格式
- **Word** (.docx) - Microsoft Word文档格式

### 报告内容包含
- 项目概述和文件结构分析
- 代码功能说明
- 技术实现细节
- 运行环境要求
- 测试用例分析

### 模板定制
1. 访问 http://localhost:5173/#/templates
2. 上传自定义模板文件
3. 在生成报告时选择对应模板

## 🔧 常见问题

### Q: 后端服务启动失败
**A:** 检查以下几点：
- 确保8000端口未被占用
- 确认Python环境和依赖已安装
- 检查`backend/requirements.txt`中的依赖

### Q: 前端页面无法访问
**A:** 
- 确保前端服务已启动
- 检查5173端口是否被占用
- 确认Node.js和npm已正确安装

### Q: 报告生成时间过长
**A:** 
- 首次生成可能需要较长时间（AI分析）
- 大型项目文件会增加生成时间
- 检查网络连接是否稳定

### Q: Word格式转换失败
**A:**
- 确保`pandoc.exe`在项目根目录
- 检查pandoc是否能正常运行
- 确认有足够权限访问文件

## 📁 目录说明

```
DocHelper/
├── backend/          # 后端服务代码
├── src/             # 前端源代码
├── outputs/         # 生成的报告文件
├── uploads/         # 上传的文件
├── templates/       # 报告模板
├── test_project/    # 测试项目文件
└── pandoc.exe      # 文档转换工具
```

## 🔨 开发相关

### 后端开发
- 使用FastAPI框架
- 支持热重载开发模式
- API文档自动生成

### 前端开发
- 基于Vue 3和Element Plus
- 使用Vite构建工具
- 支持组件化开发

### 测试
- 后端API测试脚本
- 端到端功能测试
- 性能基准测试

## 📞 技术支持

如遇到问题，请：
1. 查看控制台错误信息
2. 检查日志文件
3. 提交GitHub Issue
4. 联系项目维护者

---
*DocHelper - 智能实验报告生成专家*
