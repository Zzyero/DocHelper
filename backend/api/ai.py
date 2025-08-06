"""
AI API模块
实现AI对话功能的API端点
"""

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from services.ai_service import AIService

logger = logging.getLogger(__name__)
router = APIRouter()
ai_service = AIService()

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
