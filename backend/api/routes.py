"""
API 路由模块
实验报告自动生成工具的 API 路由定义
"""

from fastapi import APIRouter

# 创建 API 路由实例
router = APIRouter()

# 导入各个子路由模块
from . import files

# 注册子路由
router.include_router(files.router, prefix="/files", tags=["files"])

@router.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "ok"}