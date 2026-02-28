from database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    chat_messages = relationship("ChatMessage", back_populates="user")
    files = relationship("UploadedFile", back_populates="user")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String(50))  # user, assistant
    content = Column(Text)
    context_file_ids = Column(JSON, nullable=True)  # File IDs used in this conversation
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="chat_messages")

class UploadedFile(Base):
    __tablename__ = "uploaded_files"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String(255))
    original_filename = Column(String(255))
    file_path = Column(String(512))
    file_type = Column(String(50))
    file_size = Column(Integer)
    mime_type = Column(String(100))
    processed_data = Column(JSON, nullable=True)  # Parsed file content
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="files")
    analysis_results = relationship("AnalysisResult", back_populates="file")

class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("uploaded_files.id"))
    analysis_type = Column(String(100))  # statistical, trend, classification, etc.
    result_data = Column(JSON)  # Analysis results
    chart_config = Column(JSON, nullable=True)  # Chart configuration
    summary = Column(Text)  # Summary text from LLM
    created_at = Column(DateTime, default=datetime.utcnow)
    
    file = relationship("UploadedFile", back_populates="analysis_results")
