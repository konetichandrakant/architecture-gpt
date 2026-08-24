from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.architecture import Architecture
from app.schemas.prompts import PostPromptRequest, PostPromptResponse
from app.services.generation.prompts import build_edit_messages
from app.services.generation.nodes import extract_mxgraph
from app.services.llm.router import UseCase, get_model_router


class PromptService:
    """Edits an existing architecture diagram from a natural-language prompt.

    Routes through the 'edit' model fleet so diagram tweaking never has to
    wait behind the heavy generation use cases.
    """

    @classmethod
    def update_architecture(cls, request: PostPromptRequest, db: Session) -> PostPromptResponse:
        architecture = db.get(Architecture, request.architecture_id)
        if architecture is None:
            raise HTTPException(status_code=404, detail="architecture not found")

        router = get_model_router()
        result = router.run(
            UseCase.EDIT,
            build_edit_messages(request.prompt, architecture.xml_diagram),
            temperature=0.2,
        )

        updated_xml = extract_mxgraph(result.content)
        if "<mxGraphModel" not in updated_xml:
            raise HTTPException(status_code=502, detail="model did not return a valid draw.io diagram")

        architecture.xml_diagram = updated_xml
        db.commit()

        return PostPromptResponse(xml_diagram=updated_xml)
