"""
模板服务模块
实验报告自动生成工具的模板管理服务实现
"""

import logging
import os
from typing import List, Dict
from backend.utils.config import Config

logger = logging.getLogger(__name__)

class TemplateService:
    """模板服务类"""
    
    def __init__(self):
        """初始化模板服务"""
        self.config = Config()
        self.templates_dir = "templates"
        logger.info("模板服务初始化成功")
    
    def is_available(self) -> bool:
        """检查模板服务是否可用"""
        return True
    
    async def initialize_templates(self):
        """初始化模板库"""
        try:
            # 创建模板目录
            if not os.path.exists(self.templates_dir):
                os.makedirs(self.templates_dir)
                logger.info(f"创建模板目录: {self.templates_dir}")
            
            # 这里可以添加预置模板的初始化逻辑
            logger.info("模板库初始化完成")
        except Exception as e:
            logger.error(f"模板库初始化失败: {str(e)}")
    
    async def get_all_templates(self) -> List[Dict]:
        """获取所有模板列表"""
        try:
            templates = []
            
            # 这里应该实现实际的模板获取逻辑
            # 目前返回一些示例模板
            templates.append({
                "id": "default",
                "name": "默认模板",
                "description": "标准实验报告模板",
                "format": "markdown"
            })
            
            templates.append({
                "id": "academic",
                "name": "学术模板",
                "description": "学术论文格式模板",
                "format": "latex"
            })
            
            return templates
        except Exception as e:
            logger.error(f"获取模板列表失败: {str(e)}")
            raise Exception(f"获取模板列表失败: {str(e)}")
    
    async def upload_template(self, name: str, description: str, file):
        """上传自定义模板"""
        try:
            # 这里应该实现实际的模板上传逻辑
            # 目前返回一个占位符信息
            template_info = {
                "id": f"custom_{name.lower().replace(' ', '_')}",
                "name": name,
                "description": description,
                "format": "markdown"
            }
            
            logger.info(f"模板上传成功: {name}")
            return template_info
        except Exception as e:
            logger.error(f"上传模板失败: {str(e)}")
            raise Exception(f"上传模板失败: {str(e)}")