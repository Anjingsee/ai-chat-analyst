from fastapi import APIRouter, Depends, HTTPException, WebSocket
from sqlalchemy.orm import Session
from database import get_db
from schemas import ChatMessageRequest, ChatMessageResponse
from services.llm_service import LLMService
from models import ChatMessage, User
from typing import List

router = APIRouter()
llm_service = LLMService()

@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    request: ChatMessageRequest,
    db: Session = Depends(get_db),
    user_id: int = 1  # In production, get from JWT token
):
    """Send a chat message and get LLM response"""
    try:
        # Save user message
        user_message = ChatMessage(
            user_id=user_id,
            role="user",
            content=request.content,
            context_file_ids=request.file_ids
        )
        db.add(user_message)
        db.commit()
        
        # Get LLM response
        context = ""
        if request.file_ids:
            # Load file data as context
            context = await llm_service.load_file_context(request.file_ids, db)
        
        llm_response = await llm_service.get_response(
            message=request.content,
            context=context,
            conversation_history=[]
        )
        
        # Save assistant response
        assistant_message = ChatMessage(
            user_id=user_id,
            role="assistant",
            content=llm_response
        )
        db.add(assistant_message)
        db.commit()
        
        return ChatMessageResponse(
            id=assistant_message.id,
            role="assistant",
            content=llm_response,
            created_at=assistant_message.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{user_id}", response_model=List[ChatMessageResponse])
async def get_chat_history(user_id: int, db: Session = Depends(get_db)):
    """Get chat history for a user"""
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == user_id
    ).order_by(ChatMessage.created_at.asc()).all()
    return messages

@router.delete("/history/{message_id}")
async def delete_message(message_id: int, db: Session = Depends(get_db)):
    """Delete a chat message"""
    message = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    db.delete(message)
    db.commit()
    return {"message": "Message deleted successfully"}
