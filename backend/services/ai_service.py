"""
AI 服务模块
实验报告自动生成工具的 AI 服务实现
"""

import logging
from typing import Optional
import openai
from backend.utils.config import Config

logger = logging.getLogger(__name__)

class AIService:
    """AI 服务类"""
    
    def __init__(self):
        """初始化 AI 服务"""
        self.config = Config()
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """初始化 AI 客户端"""
        try:
            if self.config.OPENAI_API_KEY:
                self.client = openai.OpenAI(api_key=self.config.OPENAI_API_KEY)
                logger.info("AI 客户端初始化成功")
            else:
                logger.warning("未配置 OpenAI API Key，AI 服务不可用")
        except Exception as e:
            logger.error(f"AI 客户端初始化失败: {str(e)}")
            self.client = None
    
    def is_available(self) -> bool:
        """检查 AI 服务是否可用"""
        return self.client is not None and self.config.OPENAI_API_KEY is not None
    
    async def generate_report(self, project, template_id: Optional[str] = None, 
                            format_type: str = "markdown", custom_prompt: Optional[str] = None):
        """生成实验报告"""
        try:
            # 这里应该实现实际的 AI 报告生成逻辑
            # 目前返回一个占位符内容
            report_content = f"# {project.name}\n\n这是使用 AI 生成的实验报告。\n\n"
            report_content += "## 实验目的\n\n请在此处描述实验目的。\n\n"
            report_content += "## 实验内容\n\n请在此处描述实验内容。\n\n"
            report_content += "## 实验结果\n\n请在此处描述实验结果。\n\n"
            report_content += "## 实验总结\n\n请在此处总结实验收获。\n\n"
            
            return report_content
        except Exception as e:
            logger.error(f"生成报告失败: {str(e)}")
            raise Exception(f"生成报告失败: {str(e)}")