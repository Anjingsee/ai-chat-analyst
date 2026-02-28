import os
import json
import pandas as pd
from config import settings
from sqlalchemy.orm import Session
from models import UploadedFile
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FileService:
    async def save_file(self, content: bytes, filename: str, user_id: int, db: Session) -> UploadedFile:
        """Save uploaded file and parse content"""
        try:
            # Create upload directory
            os.makedirs(settings.upload_dir, exist_ok=True)
            
            # Generate unique filename
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            file_ext = filename.split('.')[-1]
            unique_filename = f"{user_id}_{timestamp}_{filename}"
            file_path = os.path.join(settings.upload_dir, unique_filename)
            
            # Save file
            with open(file_path, 'wb') as f:
                f.write(content)
            
            # Parse file content based on type
            processed_data = await self._parse_file(content, file_ext)
            
            # Create database record
            db_file = UploadedFile(
                user_id=user_id,
                filename=unique_filename,
                original_filename=filename,
                file_path=file_path,
                file_type=file_ext,
                file_size=len(content),
                mime_type=self._get_mime_type(file_ext),
                processed_data=processed_data
            )
            
            db.add(db_file)
            db.commit()
            db.refresh(db_file)
            
            logger.info(f"File saved: {unique_filename}")
            return db_file
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving file: {str(e)}")
            raise Exception(f"Failed to save file: {str(e)}")
    
    async def _parse_file(self, content: bytes, file_ext: str) -> dict:
        """Parse file content based on file type"""
        try:
            if file_ext.lower() == 'csv':
                df = pd.read_csv(pd.io.common.BytesIO(content))
                return {
                    "type": "csv",
                    "shape": df.shape,
                    "columns": df.columns.tolist(),
                    "head": df.head(5).to_dict('records'),
                    "dtypes": df.dtypes.astype(str).to_dict()
                }
            elif file_ext.lower() in ['xlsx', 'xls']:
                df = pd.read_excel(pd.io.common.BytesIO(content))
                return {
                    "type": "excel",
                    "shape": df.shape,
                    "columns": df.columns.tolist(),
                    "head": df.head(5).to_dict('records'),
                    "dtypes": df.dtypes.astype(str).to_dict()
                }
            elif file_ext.lower() == 'json':
                data = json.loads(content.decode('utf-8'))
                return {
                    "type": "json",
                    "data": data,
                    "preview": str(data)[:500]
                }
            elif file_ext.lower() == 'txt':
                text = content.decode('utf-8')
                return {
                    "type": "text",
                    "length": len(text),
                    "preview": text[:500]
                }
            else:
                return {"type": file_ext, "note": "File parsed but content preview not available"}
        except Exception as e:
            logger.warning(f"Could not parse file content: {str(e)}")
            return {"error": str(e)}
    
    def _get_mime_type(self, file_ext: str) -> str:
        """Get MIME type based on file extension"""
        mime_types = {
            'csv': 'text/csv',
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'xls': 'application/vnd.ms-excel',
            'json': 'application/json',
            'txt': 'text/plain',
            'pdf': 'application/pdf'
        }
        return mime_types.get(file_ext.lower(), 'application/octet-stream')
