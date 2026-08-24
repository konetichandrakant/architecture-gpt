from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.prompts import PostPromptRequest, PostPromptResponse
from app.services.prompts import PromptService

router = APIRouter()

# get the architecture xml_diagram and send it as context to the LLM
@router.post("/prompt", response_model=PostPromptResponse)
def update_architecture(request: PostPromptRequest, db: Session = Depends(get_db)):
    return PromptService.update_architecture(request, db)
