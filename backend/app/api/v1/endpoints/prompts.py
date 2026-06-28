from fastapi import APIRouter
from schemas.prompts import PostPromptRequest, PostPromptResponse
from services.prompts import PromptService

router = APIRouter()

# get the architecture xml_diagram and send it as context to the LLM
@router.post("/prompt", response_model=PostPromptResponse)
def update_architecture(request: PostPromptRequest):
    return PromptService.update_architecture(request)