import json
from sqlalchemy.orm import Session
from models import AnalysisResult, UploadedFile
from services.llm_service import LLMService
from utils.chart_generator import ChartGenerator
import logging

logger = logging.getLogger(__name__)

class AnalysisService:
    def __init__(self):
        self.llm_service = LLMService()
        self.chart_generator = ChartGenerator()
    
    async def analyze(self, file: UploadedFile, analysis_type: str, custom_rules: dict = None, chart_type: str = None, db: Session = None) -> AnalysisResult:
        """Perform analysis on uploaded file"""
        try:
            # Get file data
            file_data = file.processed_data
            
            # Generate analysis based on type
            if analysis_type == "statistical":
                analysis_result = await self._statistical_analysis(file_data)
            elif analysis_type == "trend":
                analysis_result = await self._trend_analysis(file_data)
            elif analysis_type == "custom":
                analysis_result = await self._custom_analysis(file_data, custom_rules)
            else:
                analysis_result = await self._general_analysis(file_data)
            
            # Generate summary using LLM
            summary = await self.llm_service.analyze_with_rules(
                analysis_result,
                analysis_type,
                custom_rules
            )
            
            # Generate chart configuration if requested
            chart_config = None
            if chart_type:
                chart_config = await self.chart_generator.generate_config(
                    data=analysis_result,
                    chart_type=chart_type
                )
            
            # Save analysis result
            result = AnalysisResult(
                file_id=file.id,
                analysis_type=analysis_type,
                result_data=analysis_result,
                chart_config=chart_config,
                summary=summary
            )
            
            db.add(result)
            db.commit()
            db.refresh(result)
            
            logger.info(f"Analysis completed for file {file.id}")
            return result
        except Exception as e:
            db.rollback()
            logger.error(f"Error during analysis: {str(e)}")
            raise Exception(f"Analysis failed: {str(e)}")
    
    async def _statistical_analysis(self, file_data: dict) -> dict:
        """Perform statistical analysis"""
        return {
            "analysis_type": "statistical",
            "data_summary": file_data,
            "timestamp": str(__import__('datetime').datetime.utcnow())
        }
    
    async def _trend_analysis(self, file_data: dict) -> dict:
        """Perform trend analysis"""
        return {
            "analysis_type": "trend",
            "data_summary": file_data,
            "timestamp": str(__import__('datetime').datetime.utcnow())
        }
    
    async def _custom_analysis(self, file_data: dict, rules: dict) -> dict:
        """Perform custom analysis based on user-defined rules"""
        return {
            "analysis_type": "custom",
            "rules_applied": rules,
            "data_summary": file_data,
            "timestamp": str(__import__('datetime').datetime.utcnow())
        }
    
    async def _general_analysis(self, file_data: dict) -> dict:
        """Perform general analysis"""
        return {
            "analysis_type": "general",
            "data_summary": file_data,
            "timestamp": str(__import__('datetime').datetime.utcnow())
        }
