"""
文档服务模块
实验报告自动生成工具的文档处理服务实现
"""

import logging
import os
import json
import subprocess
from typing import Optional, Dict, List
from ..utils.config import Config
import PyPDF2
import docx
from PIL import Image
import aiofiles

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
    
    async def analyze_file_content(self, file_path: str) -> Dict:
        """分析文件内容并返回结构化信息"""
        try:
            if not os.path.exists(file_path):
                raise Exception(f"文件不存在: {file_path}")
            
            file_name = os.path.basename(file_path)
            file_ext = os.path.splitext(file_name)[1].lower()
            
            analysis_result = {
                "name": file_name,
                "path": file_path,
                "size": os.path.getsize(file_path),
                "extension": file_ext,
                "content": "",
                "type": "unknown",
                "metadata": {}
            }
            
            # 根据文件类型读取内容
            if file_ext in ['.py', '.js', '.java', '.cpp', '.c', '.h', '.css', '.html', '.vue', '.ts', '.jsx', '.tsx']:
                analysis_result["type"] = "code"
                analysis_result["content"] = await self._read_text_file(file_path)
                analysis_result["metadata"]["lines"] = len(analysis_result["content"].split('\n'))
                
            elif file_ext in ['.txt', '.md']:
                analysis_result["type"] = "text"
                analysis_result["content"] = await self._read_text_file(file_path)
                
            elif file_ext == '.pdf':
                analysis_result["type"] = "pdf"
                analysis_result["content"] = await self._read_pdf_file(file_path)
                
            elif file_ext in ['.doc', '.docx']:
                analysis_result["type"] = "document"
                analysis_result["content"] = await self._read_word_file(file_path)
                
            elif file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                analysis_result["type"] = "image"
                analysis_result["content"] = await self._read_image_file(file_path)
                analysis_result["metadata"] = await self._get_image_metadata(file_path)
                
            else:
                analysis_result["type"] = "other"
                # 尝试读取为文本文件
                try:
                    analysis_result["content"] = await self._read_text_file(file_path)
                except:
                    analysis_result["content"] = f"[二进制文件或无法读取的文件类型: {file_ext}]"
            
            logger.info(f"文件分析完成: {file_name} ({analysis_result['type']})")
            return analysis_result
            
        except Exception as e:
            logger.error(f"分析文件内容失败: {str(e)}")
            raise Exception(f"分析文件内容失败: {str(e)}")
    
    async def _read_text_file(self, file_path: str) -> str:
        """读取文本文件内容"""
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            return content
        except UnicodeDecodeError:
            # 如果UTF-8失败，尝试其他编码
            try:
                async with aiofiles.open(file_path, 'r', encoding='gbk') as f:
                    content = await f.read()
                return content
            except:
                return "[无法读取的文本文件]"
        except Exception as e:
            raise Exception(f"读取文本文件失败: {str(e)}")
    
    async def _read_pdf_file(self, file_path: str) -> str:
        """读取PDF文件内容"""
        try:
            content = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    content += page.extract_text() + "\n"
            return content
        except Exception as e:
            raise Exception(f"读取PDF文件失败: {str(e)}")
    
    async def _read_word_file(self, file_path: str) -> str:
        """读取Word文件内容"""
        try:
            doc = docx.Document(file_path)
            content = ""
            for paragraph in doc.paragraphs:
                content += paragraph.text + "\n"
            return content
        except Exception as e:
            raise Exception(f"读取Word文件失败: {str(e)}")
    
    async def _read_image_file(self, file_path: str) -> str:
        """读取图片文件内容（返回描述性文本）"""
        try:
            return f"[图片文件: {os.path.basename(file_path)}]"
        except Exception as e:
            raise Exception(f"读取图片文件失败: {str(e)}")
    
    async def _get_image_metadata(self, file_path: str) -> Dict:
        """获取图片元数据"""
        try:
            with Image.open(file_path) as img:
                return {
                    "width": img.width,
                    "height": img.height,
                    "mode": img.mode,
                    "format": img.format
                }
        except Exception as e:
            return {"error": f"无法获取图片元数据: {str(e)}"}
    
    async def analyze_project_files(self, file_paths: List[str]) -> Dict:
        """分析项目中的所有文件"""
        try:
            analysis_results = []
            code_files = []
            document_files = []
            image_files = []
            other_files = []
            
            for file_path in file_paths:
                try:
                    file_analysis = await self.analyze_file_content(file_path)
                    analysis_results.append(file_analysis)
                    
                    # 按类型分类
                    if file_analysis["type"] == "code":
                        code_files.append(file_analysis)
                    elif file_analysis["type"] in ["text", "pdf", "document"]:
                        document_files.append(file_analysis)
                    elif file_analysis["type"] == "image":
                        image_files.append(file_analysis)
                    else:
                        other_files.append(file_analysis)
                except Exception as e:
                    logger.warning(f"分析文件失败 {file_path}: {str(e)}")
                    continue
            
            # 生成项目概览
            project_summary = {
                "total_files": len(analysis_results),
                "code_files_count": len(code_files),
                "document_files_count": len(document_files),
                "image_files_count": len(image_files),
                "other_files_count": len(other_files),
                "code_files": code_files,
                "document_files": document_files,
                "image_files": image_files,
                "other_files": other_files
            }
            
            logger.info(f"项目文件分析完成: {len(analysis_results)} 个文件")
            return project_summary
            
        except Exception as e:
            logger.error(f"分析项目文件失败: {str(e)}")
            raise Exception(f"分析项目文件失败: {str(e)}")
    
    async def save_report(self, content: str, project_id: str, format_type: str = "markdown"):
        """保存生成的报告"""
        try:
            # 创建输出目录
            output_dir = "outputs"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 如果需要生成word格式，先生成markdown再转换
            if format_type == "docx":
                # 先保存为markdown格式
                md_filename = f"report_{project_id}.md"
                md_file_path = os.path.join(output_dir, md_filename)
                
                with open(md_file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                
                # 使用pandoc转换为word格式
                docx_filename = f"report_{project_id}.docx"
                docx_file_path = os.path.join(output_dir, docx_filename)
                
                try:
                    # 调用pandoc进行转换
                    result = subprocess.run([
                        './pandoc.exe', 
                        md_file_path, 
                        '-o', 
                        docx_file_path
                    ], capture_output=True, text=True, timeout=30)
                    
                    if result.returncode != 0:
                        logger.error(f"pandoc转换失败: {result.stderr}")
                        raise Exception(f"pandoc转换失败: {result.stderr}")
                    
                    logger.info(f"报告转换成功: {md_file_path} -> {docx_file_path}")
                    return docx_file_path
                    
                except subprocess.TimeoutExpired:
                    logger.error("pandoc转换超时")
                    raise Exception("pandoc转换超时")
                except FileNotFoundError:
                    logger.error("pandoc.exe未找到，请确保pandoc已正确安装")
                    raise Exception("pandoc未找到，请确保已正确安装")
                except Exception as e:
                    logger.error(f"pandoc转换失败: {str(e)}")
                    raise Exception(f"pandoc转换失败: {str(e)}")
            
            else:
                # 其他格式直接保存
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
