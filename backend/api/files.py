"""
文件处理API模块
实现文件上传和解压功能
"""

import logging
import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from ..utils.file_utils import FileUtils
from typing import List
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()
file_utils = FileUtils()

@router.get("/")
async def get_files_status():
    """获取文件服务状态"""
    return {"status": "files service ready"}

@router.post("/upload-and-extract")
async def upload_and_extract(file: UploadFile = File(...)):
    """上传压缩文件并自动解压"""
    try:
        # 验证文件
        if not file.filename:
            raise HTTPException(status_code=422, detail="文件名不能为空")
        
        # 验证文件格式
        allowed_extensions = ['.zip', '.rar']
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(status_code=422, detail=f"不支持的文件格式: {file_ext}，仅支持 {', '.join(allowed_extensions)}")
        
        # 验证文件大小 (限制为100MB)
        max_size = 100 * 1024 * 1024  # 100MB
        content = await file.read()
        if len(content) > max_size:
            raise HTTPException(status_code=422, detail="文件大小超过限制 (100MB)")
        
        # 记录接收到的文件信息
        logger.info(f"接收到文件: {file.filename}, 大小: {len(content)} bytes, 类型: {file.content_type}")
        
        # 创建上传目录
        upload_dir = "uploads/temp"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        # 保存上传的文件
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        # 准备解压目录
        extract_dir = os.path.join("uploads/extracted", os.path.splitext(file.filename)[0])
        if os.path.exists(extract_dir):
            # 如果目录已存在，清空它
            import shutil
            shutil.rmtree(extract_dir)
        os.makedirs(extract_dir)
        
        # 执行解压
        extracted_files = await file_utils.extract_archive(file_path, extract_dir)
        
        # 获取解压后的文件信息
        file_info = []
        for f in extracted_files:
            full_path = os.path.join(extract_dir, f)
            if os.path.isfile(full_path):
                file_info.append({
                    "name": f,
                    "path": full_path,
                    "size": os.path.getsize(full_path)
                })
        
        # 清理上传的压缩文件
        if os.path.exists(file_path):
            os.remove(file_path)
        
        logger.info(f"解压成功: {file.filename} -> {len(file_info)} 个文件")
        
        return {
            "status": "success",
            "original_file": file.filename,
            "extracted_files": file_info,
            "count": len(file_info)
        }
    
    except HTTPException:
        # 重新抛出HTTP异常
        raise
    except Exception as e:
        logger.error(f"文件处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"文件处理失败: {str(e)}")

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """上传文件"""
    try:
        if not files:
            raise HTTPException(status_code=400, detail="请选择要上传的文件")
        
        # 创建上传目录
        upload_dir = "uploads"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        # 保存文件并分类
        uploaded_files = []
        for file in files:
            # 保存文件
            file_path = await file_utils.save_uploaded_file(file)
            
            # 分析文件类型
            file_category = file_utils.analyze_file_type(file.filename, file.content_type)
            
            uploaded_files.append({
                "name": file.filename,
                "path": file_path,
                "size": file.size or 0,
                "type": file.content_type or "application/octet-stream",
                "category": file_category,
                "lastModified": datetime.now().isoformat()
            })
        
        return {
            "success": True,
            "files": uploaded_files,
            "message": f"成功上传 {len(files)} 个文件"
        }
        
    except Exception as e:
        logger.error(f"文件上传失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")
