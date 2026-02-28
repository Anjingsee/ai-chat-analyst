import openai
from config import settings
from sqlalchemy.orm import Session
from models import UploadedFile
import json
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.model = settings.llm_model
        self.provider = settings.llm_provider
        
        if self.provider == "openai":
            openai.api_key = settings.openai_api_key
    
    async def get_response(self, message: str, context: str = "", conversation_history: list = None) -> str:
        """Get response from LLM"""
        try:
            system_prompt = f"""You are a helpful AI assistant specialized in data analysis and insights.
            
When analyzing data, you should:
1. Provide clear and concise insights
2. Highlight trends and patterns
3. Make actionable recommendations
4. Use data-driven language
"""
            if context:
                system_prompt += f"\n\nContext from uploaded files:\n{context}"
            
            messages = [{"role": "system", "content": system_prompt}]
            
            if conversation_history:
                messages.extend(conversation_history)
            
            messages.append({"role": "user", "content": message})
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error getting LLM response: {str(e)}")
            raise Exception(f"Failed to get LLM response: {str(e)}")
    
    async def load_file_context(self, file_ids: list, db: Session) -> str:
        """Load file data as context for LLM"""
        context_parts = []
        
        for file_id in file_ids:
            file = db.query(UploadedFile).filter(
                UploadedFile.id == file_id
            ).first()
            
            if file and file.processed_data:
                context_parts.append(f"\nFile: {file.filename}\n{json.dumps(file.processed_data, indent=2)}")
        
        return "\n".join(context_parts)
    
    async def analyze_with_rules(self, data: dict, analysis_type: str, rules: dict = None) -> str:
        """Analyze data according to custom rules"""
        prompt = f"""Analyze the following data with {analysis_type} analysis:

Data:
{json.dumps(data, indent=2)}
"""
        if rules:
            prompt += f"\n\nAnalysis Rules:\n{json.dumps(rules, indent=2)}"
        
        response = await self.get_response(prompt)
        return response
