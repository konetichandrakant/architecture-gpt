from pydantic import BaseModel

class PostPromptRequest(BaseModel):
    prompt: str
    architecture_id: int

class PostPromptResponse(BaseModel):
    xml_diagram: str