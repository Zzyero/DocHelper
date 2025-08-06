"""
用户设置模型模块
实验报告自动生成工具的用户设置数据模型实现
"""

import logging
import os
import json
from datetime import datetime
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class UserSettings:
    """用户设置模型类"""
    
    def __init__(self):
        """初始化用户设置"""
        self.id = "user_settings"
        self.ai_settings: Dict = {
            "apiUrl": "api-inference.modelscope.cn/v1",
            "apiKey": "",
            "modelName": "Qwen/Qwen3-235B-A22B-Thinking-2507",
            "maxTokens": 4000,
            "temperature": 0.7
        }
        self.doc_settings: Dict = {
            "defaultFormat": "markdown",
            "outputDir": "",
            "autoSave": True,
            "includeToc": True
        }
        self.app_settings: Dict = {
            "language": "zh-CN",
            "theme": "light",
            "checkUpdates": True,
            "analytics": False
        }
        self.uploaded_files: list = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """将用户设置对象转换为字典"""
        return {
            "id": self.id,
            "ai_settings": self.ai_settings,
            "doc_settings": self.doc_settings,
            "app_settings": self.app_settings,
            "uploaded_files": self.uploaded_files,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """从字典创建用户设置对象"""
        settings = cls()
        settings.id = data.get("id", "user_settings")
        settings.ai_settings = data.get("ai_settings", settings.ai_settings)
        settings.doc_settings = data.get("doc_settings", settings.doc_settings)
        settings.app_settings = data.get("app_settings", settings.app_settings)
        settings.uploaded_files = data.get("uploaded_files", [])
        settings.created_at = datetime.fromisoformat(data.get("created_at", datetime.now().isoformat()))
        settings.updated_at = datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat()))
        return settings
    
    def save(self):
        """保存用户设置"""
        try:
            # 创建数据目录
            data_dir = "data"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            
            # 保存用户设置到文件
            file_path = os.path.join(data_dir, "user_settings.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
            
            logger.info("用户设置保存成功")
        except Exception as e:
            logger.error(f"保存用户设置失败: {str(e)}")
            raise Exception(f"保存用户设置失败: {str(e)}")
    
    @classmethod
    def get_settings(cls):
        """获取用户设置"""
        try:
            data_dir = "data"
            file_path = os.path.join(data_dir, "user_settings.json")
            
            if not os.path.exists(file_path):
                # 如果设置文件不存在，创建默认设置
                settings = cls()
                settings.save()
                return settings
            
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            return cls.from_dict(data)
        except Exception as e:
            logger.error(f"获取用户设置失败: {str(e)}")
            # 返回默认设置
            return cls()
    
    def update_ai_settings(self, settings: Dict):
        """更新AI设置"""
        self.ai_settings.update(settings)
        self.updated_at = datetime.now()
    
    def update_doc_settings(self, settings: Dict):
        """更新文档设置"""
        self.doc_settings.update(settings)
        self.updated_at = datetime.now()
    
    def update_app_settings(self, settings: Dict):
        """更新应用设置"""
        self.app_settings.update(settings)
        self.updated_at = datetime.now()
    
    def update_uploaded_files(self, files: list):
        """更新上传文件列表"""
        self.uploaded_files = files
        self.updated_at = datetime.now()
