from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import AnalysisRequest, AnalysisResponse
from services.analysis_service import AnalysisService
from models import AnalysisResult, UploadedFile
from typing import List

router = APIRouter()
analysis_service = AnalysisService()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_file(
    request: AnalysisRequest,
    db: Session = Depends(get_db)
):
    """Analyze uploaded file with LLM"""
    try:
        # Check if file exists
        file = db.query(UploadedFile).filter(
            UploadedFile.id == request.file_id
        ).first()
        
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        
        # Perform analysis
        result = await analysis_service.analyze(
            file=file,
            analysis_type=request.analysis_type,
            custom_rules=request.custom_rules,
            chart_type=request.chart_type,
            db=db
        )
        
        return AnalysisResponse(
            id=result.id,
            file_id=result.file_id,
            analysis_type=result.analysis_type,
            result_data=result.result_data,
            summary=result.summary,
            created_at=result.created_at
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/results/{file_id}", response_model=List[AnalysisResponse])
async def get_analysis_results(file_id: int, db: Session = Depends(get_db)):
    """Get all analysis results for a file"""
    results = db.query(AnalysisResult).filter(
        AnalysisResult.file_id == file_id
    ).order_by(AnalysisResult.created_at.desc()).all()
    return results

@router.get("/result/{result_id}", response_model=AnalysisResponse)
async def get_analysis_result(result_id: int, db: Session = Depends(get_db)):
    """Get a specific analysis result"""
    result = db.query(AnalysisResult).filter(
        AnalysisResult.id == result_id
    ).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    return result
