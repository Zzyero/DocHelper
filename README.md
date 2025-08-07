# DocHelper - 实验报告自动生成工具

DocHelper 是一个智能实验报告自动生成工具，能够分析代码项目并生成专业的实验报告。

## 🚀 快速开始

### 一键启动开发环境

**Windows用户:**
```bash
# 使用批处理文件启动
start_dev.bat

# 或使用PowerShell脚本启动
powershell -ExecutionPolicy Bypass -File start_dev.ps1
```

**跨平台用户:**
```bash
# 使用Python脚本启动
python start_dev.py
```

### 手动启动服务

**启动后端服务:**
```bash
python -c "import sys; sys.path.append('.'); from backend.main import app; import uvicorn; uvicorn.run('backend.main:app', host='127.0.0.1', port=8000, reload=True)"
```

**启动前端服务:**
```bash
npm run dev
```

## 🌐 访问地址

- **前端页面**: http://localhost:5173
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

## 📁 项目结构

```
DocHelper/
├── backend/          # 后端服务
│   ├── api/         # API路由
│   ├── models/      # 数据模型
│   ├── services/    # 业务逻辑
│   ├── utils/       # 工具函数
│   └── main.py     # 主应用入口
├── src/             # 前端源码
│   ├── views/       # 页面组件
│   ├── components/  # 公共组件
│   ├── stores/      # 状态管理
│   └── router/      # 路由配置
├── test_project/    # 测试项目
├── outputs/         # 输出文件
└── templates/       # 报告模板
```

## 🛠️ 主要功能

### 1. 文件上传与管理
- 支持多种编程语言文件上传
- 文件列表管理
- 文件预览功能

### 2. 实验报告生成
- **AI智能分析**: 自动分析代码结构和功能
- **多格式输出**: 支持Markdown和Word格式
- **模板定制**: 可自定义报告模板

### 3. AI对话功能
- 智能问答
- 代码解释
- 技术咨询

### 4. 模板管理
- 预设模板
- 自定义模板上传
- 模板编辑

## 🔧 技术栈

### 后端
- **Python 3.12+**
- **FastAPI**: 高性能API框架
- **Uvicorn**: ASGI服务器
- **ModelScope**: AI模型服务
- **pandoc**: 文档格式转换

### 前端
- **Vue 3**: 渐进式JavaScript框架
- **Vite**: 现代化构建工具
- **Element Plus**: Vue组件库
- **Pinia**: 状态管理

## 📖 使用流程

1. **上传文件**: 在"文件上传"页面上传项目文件
2. **创建项目**: 系统自动分析文件并创建项目
3. **生成报告**: 选择模板和格式生成实验报告
4. **下载报告**: 在"历史记录"中下载生成的报告

## 🎯 特色功能

### AI驱动的报告生成
- 智能代码分析
- 自动生成技术文档
- 多语言支持

### 灵活的格式转换
- Markdown → Word (docx)
- 支持pandoc进行格式转换
- 保持文档格式和样式

### 用户友好的界面
- 响应式设计
- 直观的操作流程
- 实时状态反馈

## 📊 API接口

### 项目管理
- `POST /api/v1/projects` - 创建项目
- `GET /api/v1/projects` - 获取项目列表
- `GET /api/v1/projects/{id}` - 获取项目详情

### 报告生成
- `POST /api/v1/generate` - 生成实验报告
- `POST /api/v1/convert` - 文档格式转换

### AI服务
- `GET /api/v1/ai/status` - AI服务状态
- `POST /api/v1/ai/chat` - AI对话

## 🎨 界面预览

### 首页
![首页](screenshots/home.png)

### 文件上传
![文件上传](screenshots/upload.png)

### 报告生成
![报告生成](screenshots/generate.png)

### AI对话
![AI对话](screenshots/ai-chat.png)

## 🔒 安全特性

- CORS跨域支持
- 文件上传验证
- API接口保护
- 错误处理机制

## 📈 性能优化

- 热重载开发模式
- 异步处理
- 缓存机制
- 内存优化

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

## 📄 许可证

MIT License

## 📞 支持

如有问题，请提交 Issue 或联系开发者。

---
*DocHelper - 让实验报告生成变得更简单！*
