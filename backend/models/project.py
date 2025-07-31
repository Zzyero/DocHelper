"""
项目模型模块
实验报告自动生成工具的项目数据模型实现
"""

import logging
import os
import json
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum

logger = logging.getLogger(__name__)

class ProjectStatus(str, Enum):
    """项目状态枚举"""
    CREATED = "created"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"

class Project:
    """项目模型类"""
    
    def __init__(self, name: str, description: str = "", status: ProjectStatus = ProjectStatus.CREATED):
        """初始化项目"""
        self.id = self._generate_id()
        self.name = name
        self.description = description
        self.status = status
        self.files: List[Dict] = []
        self.output_path: Optional[str] = None
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def _generate_id(self) -> str:
        """生成项目 ID"""
        return f"proj_{int(datetime.now().timestamp() * 1000)}"
    
    def to_dict(self) -> Dict:
        """将项目对象转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "files": self.files,
            "output_path": self.output_path,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """从字典创建项目对象"""
        project = cls(
            name=data["name"],
            description=data.get("description", ""),
            status=ProjectStatus(data.get("status", ProjectStatus.CREATED))
        )
        project.id = data["id"]
        project.files = data.get("files", [])
        project.output_path = data.get("output_path")
        project.created_at = datetime.fromisoformat(data["created_at"])
        project.updated_at = datetime.fromisoformat(data["updated_at"])
        return project
    
    async def save(self):
        """保存项目信息"""
        try:
            # 创建数据目录
            data_dir = "data"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            
            # 保存项目信息到文件
            file_path = os.path.join(data_dir, f"{self.id}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
            
            logger.info(f"项目保存成功: {self.name} ({self.id})")
        except Exception as e:
            logger.error(f"保存项目失败: {str(e)}")
            raise Exception(f"保存项目失败: {str(e)}")
    
    @classmethod
    async def get_by_id(cls, project_id: str):
        """根据 ID 获取项目"""
        try:
            data_dir = "data"
            file_path = os.path.join(data_dir, f"{project_id}.json")
            
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            return cls.from_dict(data)
        except Exception as e:
            logger.error(f"获取项目失败: {str(e)}")
            return None
    
    @classmethod
    async def get_all(cls, skip: int = 0, limit: int = 10):
        """获取所有项目"""
        try:
            data_dir = "data"
            if not os.path.exists(data_dir):
                return []
            
            projects = []
            files = [f for f in os.listdir(data_dir) if f.endswith(".json")]
            
            # 按创建时间排序
            files.sort(key=lambda x: os.path.getctime(os.path.join(data_dir, x)), reverse=True)
            
            # 分页处理
            files = files[skip:skip+limit]
            
            for file in files:
                try:
                    with open(os.path.join(data_dir, file), "r", encoding="utf-8") as f:
                        data = json.load(f)
                    project = cls.from_dict(data)
                    projects.append(project)
                except Exception as e:
                    logger.error(f"加载项目失败 {file}: {str(e)}")
                    continue
            
            return projects
        except Exception as e:
            logger.error(f"获取项目列表失败: {str(e)}")
            return []