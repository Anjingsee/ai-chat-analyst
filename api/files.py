from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import FileUploadResponse
from services.file_service import FileService
from models import UploadedFile
from config import settings
from typing import List
import os

router = APIRouter()
file_service = FileService()

@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: int = 1
):
    """Upload a file for analysis"""
    try:
        # Validate file size
        content = await file.read()
        if len(content) > settings.max_file_size:
            raise HTTPException(
                status_code=413,
                detail=f"File size exceeds maximum allowed size of {settings.max_file_size} bytes"
            )
        
        # Validate file type
        file_ext = file.filename.split('.')[-1].lower()
        allowed_types = settings.allowed_file_types.split(',')
        if file_ext not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_ext} not allowed. Allowed types: {allowed_types}"
            )
        
        # Save file
        saved_file = await file_service.save_file(
            content=content,
            filename=file.filename,
            user_id=user_id,
            db=db
        )
        
        return FileUploadResponse(
            id=saved_file.id,
            filename=saved_file.filename,
            original_filename=saved_file.original_filename,
            file_size=saved_file.file_size,
            file_type=saved_file.file_type,
            created_at=saved_file.created_at
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list/{user_id}", response_model=List[FileUploadResponse])
async def list_user_files(user_id: int, db: Session = Depends(get_db)):
    """List all files uploaded by a user"""
    files = db.query(UploadedFile).filter(
        UploadedFile.user_id == user_id
    ).order_by(UploadedFile.created_at.desc()).all()
    return files

@router.get("/{file_id}")
async def get_file_content(file_id: int, db: Session = Depends(get_db)):
    """Get file content"""
    file = db.query(UploadedFile).filter(UploadedFile.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    return {
        "id": file.id,
        "filename": file.filename,
        "file_type": file.file_type,
        "processed_data": file.processed_data
    }

@router.delete("/{file_id}")
async def delete_file(file_id: int, db: Session = Depends(get_db)):
    """Delete a file"""
    file = db.query(UploadedFile).filter(UploadedFile.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Delete file from disk
    if os.path.exists(file.file_path):
        os.remove(file.file_path)
    
    db.delete(file)
    db.commit()
    return {"message": "File deleted successfully"}
