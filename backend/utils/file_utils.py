"""
文件工具模块
实验报告自动生成工具的文件处理工具实现
"""

import logging
import os
import shutil
from typing import List
from fastapi import UploadFile
import aiofiles
from backend.utils.config import Config

logger = logging.getLogger(__name__)

class FileUtils:
    """文件工具类"""
    
    def __init__(self):
        """初始化文件工具"""
        self.config = Config()
        logger.info("文件工具初始化成功")
    
    async def save_uploaded_file(self, file: UploadFile, project_id: str) -> str:
        """保存上传的文件"""
        try:
            # 创建上传目录
            upload_dir = os.path.join("uploads", project_id)
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            # 生成文件路径
            file_path = os.path.join(upload_dir, file.filename)
            
            # 保存文件
            async with aiofiles.open(file_path, 'wb') as out_file:
                content = await file.read()
                await out_file.write(content)
            
            logger.info(f"文件保存成功: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"保存上传文件失败: {str(e)}")
            raise Exception(f"保存上传文件失败: {str(e)}")
    
    async def cleanup_temp_files(self):
        """清理临时文件"""
        try:
            temp_dirs = ["temp", "uploads/temp"]
            
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                    logger.info(f"清理临时目录: {temp_dir}")
            
            logger.info("临时文件清理完成")
        except Exception as e:
            logger.error(f"清理临时文件失败: {str(e)}")
    
    async def get_file_info(self, file_path: str) -> dict:
        """获取文件信息"""
        try:
            if not os.path.exists(file_path):
                raise Exception(f"文件不存在: {file_path}")
            
            stat = os.stat(file_path)
            
            file_info = {
                "name": os.path.basename(file_path),
                "path": file_path,
                "size": stat.st_size,
                "created_at": stat.st_ctime,
                "modified_at": stat.st_mtime
            }
            
            return file_info
        except Exception as e:
            logger.error(f"获取文件信息失败: {str(e)}")
            raise Exception(f"获取文件信息失败: {str(e)}")
    
    async def read_file_content(self, file_path: str, encoding: str = "utf-8") -> str:
        """读取文件内容"""
        try:
            async with aiofiles.open(file_path, 'r', encoding=encoding) as f:
                content = await f.read()
            return content
        except Exception as e:
            logger.error(f"读取文件内容失败: {str(e)}")
            raise Exception(f"读取文件内容失败: {str(e)}")