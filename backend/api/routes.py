"""
API 路由模块
实验报告自动生成工具的 API 路由定义
"""

from fastapi import APIRouter

# 创建 API 路由实例
router = APIRouter()

# 导入各个子路由模块
# from . import projects, reports, templates, files

# 注册子路由
# router.include_router(projects.router, prefix="/projects", tags=["projects"])
# router.include_router(reports.router, prefix="/reports", tags=["reports"])
# router.include_router(templates.router, prefix="/templates", tags=["templates"])
# router.include_router(files.router, prefix="/files", tags=["files"])

@router.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "ok"}