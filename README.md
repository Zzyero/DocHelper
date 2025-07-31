# DocHelper - 实验报告自动生成工具

DocHelper 是一款基于人工智能的实验报告自动生成工具，旨在帮助学生和研究人员快速生成高质量的实验报告文档。

## 功能特性

### 🚀 核心功能
- **智能文件上传**: 支持多种文件格式，包括代码包、实验指导书、结果图片等
- **AI 驱动生成**: 基于大语言模型，自动分析实验内容并生成专业报告
- **丰富模板库**: 提供多种报告模板，支持自定义样式和格式标准化
- **多格式导出**: 支持 PDF、Word、Markdown 等多种格式输出
- **实时预览**: 支持文档实时预览和编辑

### 🎨 用户界面
- **Windows 11 风格**: 采用现代简约的 Fluent Design 设计语言
- **响应式布局**: 完美适配不同屏幕尺寸
- **直观操作**: 拖拽上传、一键生成、便捷管理

### 🔧 技术特性
- **跨平台支持**: 基于 Electron 构建，支持 Windows、macOS、Linux
- **本地部署**: 数据完全本地存储，保护隐私安全
- **模块化架构**: 前后端分离，易于扩展和维护
- **OpenAI 兼容**: 支持多种 AI 模型接口

## 技术架构

### 前端技术栈
- **Vue 3**: 现代化的前端框架
- **Element Plus**: 企业级 UI 组件库
- **Vite**: 快速的构建工具
- **Electron**: 跨平台桌面应用框架
- **Pinia**: 状态管理
- **Vue Router**: 路由管理

### 后端技术栈
- **Python 3.8+**: 后端开发语言
- **FastAPI**: 现代化的 Web 框架
- **SQLAlchemy**: ORM 数据库操作
- **Pandoc**: 文档格式转换
- **LaTeX**: PDF 文档生成
- **OpenAI API**: AI 模型接口

### 文档处理
- **Markdown**: 轻量级标记语言
- **LaTeX**: 专业文档排版系统
- **Pandoc**: 通用文档转换器
- **python-docx**: Word 文档处理
- **PyPDF2**: PDF 文档处理

## 项目结构

```
DocHelper/
├── frontend/                 # Vue 前端应用
│   ├── src/
│   │   ├── components/      # 可复用组件
│   │   ├── views/          # 页面组件
│   │   ├── router/         # 路由配置
│   │   ├── store/          # 状态管理
│   │   └── utils/          # 工具函数
│   ├── electron/           # Electron 主进程
│   └── dist/              # 构建输出
├── backend/                # Python 后端服务
│   ├── api/               # API 路由
│   ├── services/          # 业务逻辑服务
│   ├── models/            # 数据模型
│   ├── utils/             # 工具函数
│   └── templates/         # 报告模板
├── templates/             # 文档模板库
├── docs/                  # 项目文档
└── scripts/              # 构建和部署脚本
```

## 快速开始

### 环境要求
- **Node.js**: 16.0 或更高版本
- **Python**: 3.8 或更高版本
- **Pandoc**: 2.0 或更高版本
- **LaTeX**: MiKTeX 或 TeX Live

### 安装依赖

#### 前端依赖
```bash
npm install
```

#### 后端依赖
```bash
cd backend
pip install -r requirements.txt
```

### 开发环境运行

#### 启动后端服务
```bash
cd backend
python main.py
```

#### 启动前端开发服务器
```bash
npm run dev
```

#### 启动 Electron 应用
```bash
npm run dev:electron
```

### 构建和打包

#### 构建前端
```bash
npm run build
```

#### 打包 Electron 应用
```bash
npm run build:electron
```

## 核心模块说明

### 1. 文件上传模块 (`src/views/Upload.vue`)
- **功能**: 处理多种类型文件的上传和分类
- **特性**: 拖拽上传、文件预览、自动分类
- **支持格式**: 代码文件、文档、图片、压缩包

### 2. AI 生成模块 (`backend/services/ai_service.py`)
- **功能**: 调用大语言模型生成实验报告
- **特性**: 多模型支持、自定义提示词、流式输出
- **待实现**: OpenAI API 集成、本地模型支持

### 3. 文档处理模块 (`backend/services/document_service.py`)
- **功能**: 文档格式转换和处理
- **特性**: Markdown/LaTeX/Word 互转、模板应用
- **待实现**: Pandoc 集成、LaTeX 编译

### 4. 模板管理模块 (`backend/services/template_service.py`)
- **功能**: 管理文档模板和样式
- **特性**: 预置模板、自定义模板、样式标准化
- **待实现**: VBA 段落聚类、样式自动识别

### 5. 项目管理模块 (`backend/models/project.py`)
- **功能**: 项目生命周期管理
- **特性**: 项目创建、状态跟踪、历史记录
- **待实现**: 数据库持久化、项目导入导出

### 6. 设置管理模块 (`src/views/Settings.vue`)
- **功能**: 应用配置和参数管理
- **特性**: AI 模型配置、文档设置、应用偏好
- **已实现**: 本地存储、配置验证

## 待实现功能

### 高优先级
1. **AI 服务集成**: 完成 OpenAI API 调用逻辑
2. **文档转换**: 实现 Pandoc 和 LaTeX 集成
3. **数据持久化**: 完成 SQLite 数据库集成
4. **文件处理**: 完善文件读取和解析功能

### 中优先级
1. **模板系统**: 实现模板库和自定义模板功能
2. **VBA 处理**: Word 模板样式自动标准化
3. **批量处理**: 支持多个项目批量生成
4. **导出优化**: 优化各种格式的导出质量

### 低优先级
1. **插件系统**: 支持第三方插件扩展
2. **云端同步**: 可选的云端数据同步
3. **协作功能**: 多用户协作编辑
4. **版本控制**: 文档版本管理和对比

## 开发指南

### 代码规范
- **前端**: 使用 ESLint + Prettier 进行代码格式化
- **后端**: 使用 Black + Flake8 进行代码检查
- **提交**: 使用 Conventional Commits 规范

### 目录命名
- 使用小写字母和下划线
- 组件文件使用 PascalCase
- 工具函数使用 camelCase

### API 设计
- RESTful API 设计原则
- 统一的响应格式
- 完整的错误处理

## 部署说明

### 开发环境
1. 克隆项目到本地
2. 安装前后端依赖
3. 配置环境变量
4. 启动开发服务器

### 生产环境
1. 构建前端静态文件
2. 打包 Electron 应用
3. 配置生产环境参数
4. 生成安装包

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

### 提交流程
1. Fork 项目
2. 创建功能分支
3. 提交代码更改
4. 创建 Pull Request

### 问题反馈
- 使用 GitHub Issues 报告 Bug
- 详细描述问题和复现步骤
- 提供相关的错误日志

## 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

## 联系方式

- **项目主页**: https://github.com/dochelper/dochelper
- **问题反馈**: https://github.com/dochelper/dochelper/issues
- **技术支持**: support@dochelper.com

---

**注意**: 本项目目前处于开发阶段，部分功能尚未完全实现。欢迎开发者参与贡献！
