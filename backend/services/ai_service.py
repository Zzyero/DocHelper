"""
AI 服务模块
实验报告自动生成工具的 AI 服务实现
"""

import logging
from typing import Optional
import openai
from utils.config import Config
from models.user_settings import UserSettings

logger = logging.getLogger(__name__)

class AIService:
    """AI 服务类"""
    
    def __init__(self):
        """初始化 AI 服务"""
        self.config = Config()
        self.client = None
        self.user_settings = None
        self._initialize_client()
    
    def _get_api_key(self) -> Optional[str]:
        """获取API密钥，优先使用用户设置中的密钥"""
        # 首先尝试从用户设置获取
        try:
            user_settings = UserSettings.get_settings()
            api_key = user_settings.ai_settings.get('apiKey')
            if api_key and api_key.strip():
                return api_key.strip()
        except Exception as e:
            logger.warning(f"获取用户设置失败: {str(e)}")
        
        # 如果用户设置中没有，则使用环境变量
        return self.config.OPENAI_API_KEY
    
    def _get_api_base(self) -> str:
        """获取API基础URL"""
        try:
            user_settings = UserSettings.get_settings()
            if user_settings and user_settings.ai_settings.get('apiUrl'):
                api_url = user_settings.ai_settings.get('apiUrl').strip()
                if api_url:
                    # 确保URL格式正确
                    if not api_url.startswith('http'):
                        # 检查是否是相对路径或需要特定处理的URL
                        if api_url.startswith('api-inference.modelscope.cn'):
                            api_url = 'https://' + api_url
                        else:
                            api_url = 'https://' + api_url
                    return api_url
        except Exception as e:
            logger.warning(f"获取API URL失败: {str(e)}")
        
        # 使用配置中的默认值
        return self.config.OPENAI_API_BASE
    
    def _get_model_name(self) -> str:
        """获取模型名称"""
        try:
            user_settings = UserSettings.get_settings()
            if user_settings and user_settings.ai_settings.get('modelName'):
                model_name = user_settings.ai_settings.get('modelName').strip()
                if model_name:
                    return model_name
        except Exception as e:
            logger.warning(f"获取模型名称失败: {str(e)}")
        
        # 使用配置中的默认值
        return self.config.OPENAI_MODEL
    
    def _initialize_client(self):
        """初始化 AI 客户端"""
        try:
            api_key = self._get_api_key()
            api_base = self._get_api_base()
            
            if api_key:
                self.client = openai.OpenAI(
                    api_key=api_key,
                    base_url=api_base
                )
                logger.info(f"AI 客户端初始化成功，使用API地址: {api_base}")
            else:
                logger.warning("未配置 OpenAI API Key，AI 服务不可用")
        except Exception as e:
            logger.error(f"AI 客户端初始化失败: {str(e)}")
            self.client = None
    
    def is_available(self) -> bool:
        """检查 AI 服务是否可用"""
        api_key = self._get_api_key()
        return self.client is not None and api_key is not None
    
    async def generate_report(self, project, template_id: Optional[str] = None, 
                            format_type: str = "markdown", custom_prompt: Optional[str] = None):
        """生成实验报告"""
        try:
            # 构建提示词
            prompt = f"""请为以下实验项目生成一份详细的实验报告：

项目名称：{project.name}
项目描述：{project.description}

实验文件：
{chr(10).join([f"- {file['name']}" for file in project.files])}

请按照以下结构生成报告：
1. 实验目的
2. 实验内容
3. 实验步骤
4. 实验结果
5. 实验分析
6. 实验总结

要求：
- 内容详实，逻辑清晰
- 语言专业，格式规范
- 根据实验文件内容生成具体的分析
- 报告长度不少于1000字
"""
            
            if custom_prompt:
                prompt = custom_prompt
            
            # 调用AI模型生成报告
            if self.client:
                response = self.client.chat.completions.create(
                    model=self._get_model_name(),
                    messages=[
                        {"role": "system", "content": "你是一位专业的实验报告写作助手，请生成格式规范、内容详实的实验报告。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=4000
                )
                
                report_content = response.choices[0].message.content
                return report_content
            else:
                # 如果AI服务不可用，返回占位符内容
                report_content = f"# {project.name}\n\n这是使用 AI 生成的实验报告。\n\n"
                report_content += "## 实验目的\n\n请在此处描述实验目的。\n\n"
                report_content += "## 实验内容\n\n请在此处描述实验内容。\n\n"
                report_content += "## 实验结果\n\n请在此处描述实验结果。\n\n"
                report_content += "## 实验总结\n\n请在此处总结实验收获。\n\n"
                return report_content
                
        except Exception as e:
            logger.error(f"生成报告失败: {str(e)}")
            raise Exception(f"生成报告失败: {str(e)}")
