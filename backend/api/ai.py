"""
AI API模块
实现AI对话功能和报告生成的API端点
"""

import logging
from fastapi import APIRouter, HTTPException, Form
from pydantic import BaseModel
from typing import List, Optional
from services.ai_service import AIService
from services.document_service import DocumentService
import json
import os

logger = logging.getLogger(__name__)
router = APIRouter()
ai_service = AIService()
document_service = DocumentService()

class ChatMessage(BaseModel):
    """聊天消息模型"""
    id: Optional[int] = None
    role: str  # 'user' 或 'ai'
    content: str

class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str
    history: List[ChatMessage] = []

class ChatResponse(BaseModel):
    """聊天响应模型"""
    reply: str

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """与AI进行对话"""
    try:
        # 检查AI服务是否可用
        if not ai_service.is_available():
            raise HTTPException(
                status_code=503, 
                detail="AI服务不可用，请检查OpenAI API Key配置"
            )
        
        # 构建对话历史
        messages = []
        for msg in request.history:
            if msg.role == 'user':
                messages.append({"role": "user", "content": msg.content})
            elif msg.role == 'ai':
                messages.append({"role": "assistant", "content": msg.content})
        
        # 添加当前用户消息
        messages.append({"role": "user", "content": request.message})
        
        # 调用AI服务
        if ai_service.client:
            # 使用用户设置中的模型名称
            model = ai_service._get_model_name()
            
            response = ai_service.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            reply = response.choices[0].message.content
            
            logger.info(f"AI对话成功: 用户消息='{request.message}', AI回复长度={len(reply)}")
            
            return ChatResponse(reply=reply)
        else:
            raise HTTPException(status_code=503, detail="AI客户端未初始化")
            
    except HTTPException:
        # 重新抛出HTTP异常
        raise
    except Exception as e:
        logger.error(f"AI对话失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI对话失败: {str(e)}")

@router.get("/status")
async def get_ai_status():
    """获取AI服务状态"""
    try:
        is_available = ai_service.is_available()
        return {
            "status": "available" if is_available else "unavailable",
            "available": is_available,
            "message": "AI服务可用" if is_available else "AI服务不可用，请检查配置"
        }
    except Exception as e:
        logger.error(f"获取AI状态失败: {str(e)}")
        return {
            "status": "error",
            "available": False,
            "message": f"获取状态失败: {str(e)}"
        }

class GenerateReportRequest(BaseModel):
    """报告生成请求模型"""
    project_name: str
    file_paths: List[str]
    template_id: Optional[str] = None
    format_type: str = "markdown"
    custom_prompt: Optional[str] = None

class GenerateReportResponse(BaseModel):
    """报告生成响应模型"""
    success: bool
    report_content: str
    output_path: Optional[str] = None
    message: str

@router.post("/generate-report", response_model=GenerateReportResponse)
async def generate_report(request: GenerateReportRequest):
    """生成实验报告"""
    try:
        # 检查AI服务是否可用
        if not ai_service.is_available():
            raise HTTPException(
                status_code=503, 
                detail="AI服务不可用，请检查OpenAI API Key配置"
            )
        
        # 检查文件是否存在
        for file_path in request.file_paths:
            if not os.path.exists(file_path):
                raise HTTPException(
                    status_code=404, 
                    detail=f"文件不存在: {file_path}"
                )
        
        # 分析项目文件内容
        logger.info(f"开始分析项目文件，共 {len(request.file_paths)} 个文件")
        project_analysis = await document_service.analyze_project_files(request.file_paths)
        
        # 构建项目信息
        project_info = {
            "name": request.project_name,
            "created_at": "2025-01-01",  # 实际项目中应该使用真实时间
            "file_count": len(request.file_paths)
        }
        
        # 调用AI服务生成报告
        logger.info("开始调用AI服务生成报告")
        report_content = await ai_service.generate_report(
            project_analysis=project_analysis,
            project_info=project_info,
            template_id=request.template_id,
            format_type=request.format_type,
            custom_prompt=request.custom_prompt
        )
        
        # 保存生成的报告
        # 使用项目名称作为ID的一部分
        project_id = request.project_name.replace(" ", "_").lower()
        output_path = await document_service.save_report(
            content=report_content,
            project_id=project_id,
            format_type=request.format_type
        )
        
        logger.info(f"报告生成成功: {output_path}")
        
        return GenerateReportResponse(
            success=True,
            report_content=report_content,
            output_path=output_path,
            message="报告生成成功"
        )
        
    except HTTPException:
        # 重新抛出HTTP异常
        raise
    except Exception as e:
        logger.error(f"生成报告失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"生成报告失败: {str(e)}")
