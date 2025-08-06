"""
配置模块
实验报告自动生成工具的配置管理实现
"""

import os
from typing import Optional

class Config:
    """配置类"""
    
    def __init__(self):
        """初始化配置"""
        # OpenAI 配置
        self.OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
        self.OPENAI_API_BASE: str = os.getenv("OPENAI_API_BASE", "https://api-inference.modelscope.cn/v1")
        self.OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "Qwen/Qwen3-235B-A22B-Thinking-2507")
        
        # 应用配置
        self.APP_NAME: str = os.getenv("APP_NAME", "DocHelper")
        self.APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
        self.DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
        
        # 数据库配置
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")
        
        # 文件路径配置
        self.UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
        self.OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "./outputs")
        self.TEMPLATE_DIR: str = os.getenv("TEMPLATE_DIR", "./templates")
        
        # 其他配置
        self.MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
        self.ALLOWED_EXTENSIONS: list = os.getenv(
            "ALLOWED_EXTENSIONS", 
            "py,js,java,cpp,c,h,css,html,vue,ts,jsx,tsx,pdf,doc,docx,txt,md,jpg,png,gif"
        ).split(",")
