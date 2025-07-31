"""
文档服务模块
实验报告自动生成工具的文档处理服务实现
"""

import logging
import os
from typing import Optional
from backend.utils.config import Config

logger = logging.getLogger(__name__)

class DocumentService:
    """文档服务类"""
    
    def __init__(self):
        """初始化文档服务"""
        self.config = Config()
        logger.info("文档服务初始化成功")
    
    def is_available(self) -> bool:
        """检查文档服务是否可用"""
        return True
    
    async def save_report(self, content: str, project_id: str, format_type: str = "markdown"):
        """保存生成的报告"""
        try:
            # 创建输出目录
            output_dir = "outputs"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 根据格式类型确定文件扩展名
            extension_map = {
                "markdown": "md",
                "html": "html",
                "pdf": "pdf",
                "docx": "docx"
            }
            extension = extension_map.get(format_type, "md")
            
            # 生成文件名
            filename = f"report_{project_id}.{extension}"
            file_path = os.path.join(output_dir, filename)
            
            # 保存文件
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            logger.info(f"报告保存成功: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"保存报告失败: {str(e)}")
            raise Exception(f"保存报告失败: {str(e)}")
    
    async def convert_document(self, input_path: str, output_format: str, template_path: Optional[str] = None):
        """文档格式转换"""
        try:
            # 这里应该实现实际的文档转换逻辑
            # 目前返回一个占位符内容
            output_dir = "outputs"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 生成输出文件名
            filename = f"converted_{os.path.basename(input_path)}.{output_format}"
            output_path = os.path.join(output_dir, filename)
            
            # 创建占位符文件
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"这是从 {input_path} 转换而来的 {output_format} 格式文档。\n")
            
            logger.info(f"文档转换成功: {input_path} -> {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"文档转换失败: {str(e)}")
            raise Exception(f"文档转换失败: {str(e)}")