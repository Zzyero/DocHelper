"""
DocHelper 后端服务
实验报告自动生成工具的 Python 后端
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
import json
import asyncio
from typing import List, Optional
from datetime import datetime
import logging

from api.routes import router as api_router
from services.ai_service import AIService
from services.document_service import DocumentService
from services.template_service import TemplateService
from models.project import Project, ProjectStatus
from utils.file_utils import FileUtils
from utils.config import Config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建 FastAPI 应用
app = FastAPI(
    title="DocHelper API",
    description="实验报告自动生成工具后端服务",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 包含 API 路由
app.include_router(api_router, prefix="/api/v1")

# 全局变量
config = Config()
ai_service = AIService()
document_service = DocumentService()
template_service = TemplateService()
file_utils = FileUtils()

@app.on_event("startup")
async def startup_event():
    """应用启动时的初始化操作"""
    logger.info("DocHelper 后端服务启动中...")
    
    # 创建必要的目录
    directories = [
        "uploads",
        "outputs",
        "templates",
        "temp",
        "static"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"创建目录: {directory}")
    
    # 初始化模板库
    await template_service.initialize_templates()
    
    logger.info("DocHelper 后端服务启动完成")

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的清理操作"""
    logger.info("DocHelper 后端服务关闭中...")
    
    # 清理临时文件
    await file_utils.cleanup_temp_files()
    
    logger.info("DocHelper 后端服务已关闭")

@app.get("/")
async def root():
    """根路径，返回服务状态"""
    return {
        "message": "DocHelper API 服务运行中",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "ai_service": ai_service.is_available(),
            "document_service": document_service.is_available(),
            "template_service": template_service.is_available()
        }
    }

# 项目管理接口
@app.post("/api/v1/projects")
async def create_project(
    name: str = Form(...),
    description: str = Form(""),
    file_paths: List[str] = Form(...)
):
    """创建新项目（基于已存在的文件路径）"""
    try:
        # 创建项目实例
        project = Project(
            name=name,
            description=description,
            status=ProjectStatus.CREATED
        )
        
        # 验证文件路径并构建文件信息
        uploaded_files = []
        for file_path in file_paths:
            if not os.path.exists(file_path):
                raise HTTPException(status_code=404, detail=f"文件不存在: {file_path}")
            
            # 获取文件信息
            file_stat = os.stat(file_path)
            uploaded_files.append({
                "name": os.path.basename(file_path),
                "path": file_path,
                "size": file_stat.st_size,
                "type": "application/octet-stream"  # 实际应用中应该根据文件扩展名确定类型
            })
        
        project.files = uploaded_files
        
        # 保存项目信息
        await project.save()
        
        logger.info(f"创建项目成功: {project.name} (ID: {project.id})")
        
        return {
            "success": True,
            "project": project.to_dict(),
            "message": "项目创建成功"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建项目失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建项目失败: {str(e)}")

@app.get("/api/v1/projects")
async def get_projects(skip: int = 0, limit: int = 10):
    """获取项目列表"""
    try:
        projects = await Project.get_all(skip=skip, limit=limit)
        return {
            "success": True,
            "projects": [project.to_dict() for project in projects],
            "total": len(projects)
        }
    except Exception as e:
        logger.error(f"获取项目列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取项目列表失败: {str(e)}")

@app.get("/api/v1/projects/{project_id}")
async def get_project(project_id: str):
    """获取项目详情"""
    try:
        project = await Project.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")
        
        return {
            "success": True,
            "project": project.to_dict()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取项目详情失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取项目详情失败: {str(e)}")

# AI 生成接口
@app.post("/api/v1/generate")
async def generate_report(
    project_id: str = Form(...),
    template_id: Optional[str] = Form(None),
    format_type: str = Form("markdown"),
    custom_prompt: Optional[str] = Form(None)
):
    """生成实验报告"""
    try:
        # 获取项目信息
        project = await Project.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")
        
        # 检查项目文件
        if not project.files:
            raise HTTPException(status_code=400, detail="项目没有文件")
        
        # 更新项目状态
        project.status = ProjectStatus.GENERATING
        project.updated_at = datetime.now()
        await project.save()
        
        # 提取文件路径
        file_paths = [file_info["path"] for file_info in project.files if os.path.exists(file_info["path"])]
        if not file_paths:
            raise HTTPException(status_code=400, detail="项目文件不存在")
        
        # 分析项目文件内容
        logger.info(f"开始分析项目文件，共 {len(file_paths)} 个文件")
        project_analysis = await document_service.analyze_project_files(file_paths)
        
        # 构建项目信息
        project_info = {
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at.isoformat() if project.created_at else datetime.now().isoformat(),
            "file_count": len(project.files)
        }
        
        # 调用 AI 服务生成报告
        report_content = await ai_service.generate_report(
            project_analysis=project_analysis,
            project_info=project_info,
            template_id=template_id,
            format_type=format_type,
            custom_prompt=custom_prompt
        )
        
        # 保存生成的报告
        output_path = await document_service.save_report(
            content=report_content,
            project_id=project_id,
            format_type=format_type
        )
        
        # 更新项目状态和结果
        project.status = ProjectStatus.COMPLETED
        project.output_path = output_path
        project.updated_at = datetime.now()
        await project.save()
        
        logger.info(f"报告生成成功: {project.name} -> {output_path}")
        
        return {
            "success": True,
            "project": project.to_dict(),
            "output_path": output_path,
            "report_content": report_content,
            "message": "报告生成成功"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"生成报告失败: {str(e)}")
        
        # 更新项目状态为失败
        try:
            project = await Project.get_by_id(project_id)
            if project:
                project.status = ProjectStatus.FAILED
                project.updated_at = datetime.now()
                await project.save()
        except:
            pass
        
        raise HTTPException(status_code=500, detail=f"生成报告失败: {str(e)}")

# 文档转换接口
@app.post("/api/v1/convert")
async def convert_document(
    input_path: str = Form(...),
    output_format: str = Form(...),
    template_path: Optional[str] = Form(None)
):
    """文档格式转换"""
    try:
        output_path = await document_service.convert_document(
            input_path=input_path,
            output_format=output_format,
            template_path=template_path
        )
        
        return {
            "success": True,
            "output_path": output_path,
            "message": "文档转换成功"
        }
        
    except Exception as e:
        logger.error(f"文档转换失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"文档转换失败: {str(e)}")

# 模板管理接口
@app.get("/api/v1/templates")
async def get_templates():
    """获取模板列表"""
    try:
        templates = await template_service.get_all_templates()
        return {
            "success": True,
            "templates": templates
        }
    except Exception as e:
        logger.error(f"获取模板列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取模板列表失败: {str(e)}")

@app.post("/api/v1/templates")
async def upload_template(
    name: str = Form(...),
    description: str = Form(""),
    file: UploadFile = File(...)
):
    """上传自定义模板"""
    try:
        template_info = await template_service.upload_template(
            name=name,
            description=description,
            file=file
        )
        
        return {
            "success": True,
            "template": template_info,
            "message": "模板上传成功"
        }
        
    except Exception as e:
        logger.error(f"上传模板失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"上传模板失败: {str(e)}")

# 文件下载接口
@app.get("/api/v1/download/{file_path:path}")
async def download_file(file_path: str):
    """下载文件"""
    try:
        full_path = os.path.join("outputs", file_path)
        if not os.path.exists(full_path):
            raise HTTPException(status_code=404, detail="文件不存在")
        
        return FileResponse(
            path=full_path,
            filename=os.path.basename(full_path)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"下载文件失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"下载文件失败: {str(e)}")

if __name__ == "__main__":
    # 开发环境运行
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
