"""
AI 服务模块
实验报告自动生成工具的 AI 服务实现
"""

import logging
from typing import Optional, Dict
import openai
from ..utils.config import Config
from ..models.user_settings import UserSettings

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
    
    async def generate_report(self, project_analysis: Dict, project_info: Dict, template_id: Optional[str] = None, 
                            format_type: str = "markdown", custom_prompt: Optional[str] = None):
        """生成实验报告"""
        try:
            # 构建详细的提示词
            system_prompt = """你是一位专业的实验报告写作助手，具有丰富的计算机科学和工程实验经验。请根据提供的实验文件内容，生成一份结构完整、内容详实、逻辑清晰的实验报告。"""
            
            # 构建用户提示词
            if custom_prompt:
                user_prompt = custom_prompt
            else:
                user_prompt = self._build_report_prompt(project_analysis, project_info)
            
            # 调用AI模型生成报告
            if self.client:
                response = self.client.chat.completions.create(
                    model=self._get_model_name(),
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=4000
                )
                
                report_content = response.choices[0].message.content
                return report_content
            else:
                # 如果AI服务不可用，返回占位符内容
                report_content = f"# {project_info.get('name', '实验报告')}\n\n这是使用 AI 生成的实验报告。\n\n"
                report_content += "## 实验目的\n\n请在此处描述实验目的。\n\n"
                report_content += "## 实验内容\n\n请在此处描述实验内容。\n\n"
                report_content += "## 实验结果\n\n请在此处描述实验结果。\n\n"
                report_content += "## 实验总结\n\n请在此处总结实验收获。\n\n"
                return report_content
                
        except Exception as e:
            logger.error(f"生成报告失败: {str(e)}")
            raise Exception(f"生成报告失败: {str(e)}")
    
    def _build_report_prompt(self, project_analysis: Dict, project_info: Dict) -> str:
        """构建报告生成的提示词"""
        prompt = f"""请为以下实验项目生成一份详细的实验报告：

## 项目基本信息
项目名称：{project_info.get('name', '未命名项目')}
创建时间：{project_info.get('created_at', '未知')}

## 项目文件概览
- 总文件数：{project_analysis.get('total_files', 0)} 个
- 代码文件：{project_analysis.get('code_files_count', 0)} 个
- 文档文件：{project_analysis.get('document_files_count', 0)} 个
- 图片文件：{project_analysis.get('image_files_count', 0)} 个
- 其他文件：{project_analysis.get('other_files_count', 0)} 个

## 详细文件内容分析
"""
        
        # 添加代码文件内容
        code_files = project_analysis.get('code_files', [])
        if code_files:
            prompt += "\n### 代码文件内容\n"
            for file_info in code_files[:3]:  # 限制前3个文件
                prompt += f"\n文件名：{file_info['name']}\n"
                prompt += f"文件类型：{file_info['extension']}\n"
                prompt += f"代码内容：\n```\n{file_info['content'][:2000]}...\n```\n"  # 限制内容长度
        
        # 添加文档文件内容
        document_files = project_analysis.get('document_files', [])
        if document_files:
            prompt += "\n### 文档文件内容\n"
            for file_info in document_files[:2]:  # 限制前2个文件
                prompt += f"\n文件名：{file_info['name']}\n"
                prompt += f"文件类型：{file_info['extension']}\n"
                prompt += f"文档内容：\n{file_info['content'][:1000]}...\n"  # 限制内容长度
        
        # 添加图片文件信息
        image_files = project_analysis.get('image_files', [])
        if image_files:
            prompt += "\n### 图片文件\n"
            for file_info in image_files[:5]:  # 限制前5个文件
                prompt += f"- {file_info['name']} ({file_info.get('metadata', {}).get('width', '未知')}x{file_info.get('metadata', {}).get('height', '未知')})\n"
        
        # 添加其他文件信息
        other_files = project_analysis.get('other_files', [])
        if other_files:
            prompt += "\n### 其他文件\n"
            for file_info in other_files[:3]:  # 限制前3个文件
                prompt += f"- {file_info['name']}\n"
        
        prompt += f"""

## 报告要求
请按照以下结构生成Markdown格式的实验报告：

1. # 实验报告标题
2. ## 实验目的
   - 简述实验的目标和意义
3. ## 实验环境
   - 列出使用的开发工具、编程语言、框架等
4. ## 实验内容
   - 详细描述实验的主要内容和实现方法
5. ## 实验步骤
   - 分步骤描述实验的实施过程
6. ## 实验结果
   - 展示实验的输出结果和运行效果
7. ## 实验分析
   - 对实验结果进行分析和讨论
8. ## 实验总结
   - 总结实验收获和遇到的问题及解决方案
9. ## 参考文献
   - 列出参考的资料和文献

## 特别要求
- 内容详实，逻辑清晰，语言专业
- 结合具体的代码和文档内容进行分析
- 报告长度不少于1500字
- 使用Markdown格式，包含适当的标题、列表、代码块等
- 如果有代码文件，请分析关键代码片段
- 如果有文档文件，请结合文档内容进行分析

请根据以上信息生成高质量的实验报告：
"""
        
        return prompt
