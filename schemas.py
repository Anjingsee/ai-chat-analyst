from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class ChatMessageRequest(BaseModel):
    content: str
    file_ids: Optional[List[int]] = None

class ChatMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class FileUploadResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_size: int
    file_type: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class AnalysisRequest(BaseModel):
    file_id: int
    analysis_type: str  # statistical, trend, classification, custom
    custom_rules: Optional[Dict[str, Any]] = None
    chart_type: Optional[str] = None  # bar, line, pie, scatter, heatmap

class AnalysisResponse(BaseModel):
    id: int
    file_id: int
    analysis_type: str
    result_data: Dict[str, Any]
    summary: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
