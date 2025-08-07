"""
设置 API模块
实现用户设置保存和获取的API端点
"""

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from ..models.user_settings import UserSettings

logger = logging.getLogger(__name__)
router = APIRouter()

class SettingsRequest(BaseModel):
    """设置请求模型"""
    ai_settings: Optional[Dict] = None
    doc_settings: Optional[Dict] = None
    app_settings: Optional[Dict] = None
    uploaded_files: Optional[List] = None

class SettingsResponse(BaseModel):
    """设置响应模型"""
    ai_settings: Dict
    doc_settings: Dict
    app_settings: Dict
    uploaded_files: List
    created_at: str
    updated_at: str

@router.get("/user-settings", response_model=SettingsResponse)
async def get_user_settings():
    """获取用户设置"""
    try:
        settings = UserSettings.get_settings()
        return SettingsResponse(
            ai_settings=settings.ai_settings,
            doc_settings=settings.doc_settings,
            app_settings=settings.app_settings,
            uploaded_files=settings.uploaded_files,
            created_at=settings.created_at.isoformat(),
            updated_at=settings.updated_at.isoformat()
        )
    except Exception as e:
        logger.error(f"获取用户设置失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取用户设置失败: {str(e)}")

@router.post("/user-settings")
async def save_user_settings(request: SettingsRequest):
    """保存用户设置"""
    try:
        # 获取现有设置
        settings = UserSettings.get_settings()
        
        # 更新设置
        if request.ai_settings is not None:
            settings.update_ai_settings(request.ai_settings)
        
        if request.doc_settings is not None:
            settings.update_doc_settings(request.doc_settings)
        
        if request.app_settings is not None:
            settings.update_app_settings(request.app_settings)
        
        if request.uploaded_files is not None:
            settings.update_uploaded_files(request.uploaded_files)
        
        # 保存设置
        settings.save()
        
        logger.info("用户设置保存成功")
        return {"message": "设置保存成功", "status": "success"}
        
    except Exception as e:
        logger.error(f"保存用户设置失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"保存用户设置失败: {str(e)}")

@router.delete("/user-settings")
async def reset_user_settings():
    """重置用户设置"""
    try:
        # 创建新的默认设置
        settings = UserSettings()
        settings.save()
        
        logger.info("用户设置已重置")
        return {"message": "设置已重置", "status": "success"}
        
    except Exception as e:
        logger.error(f"重置用户设置失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"重置用户设置失败: {str(e)}")
