from sqlalchemy.orm import Session

from app.schemas.prompts import PostPromptRequest, PostPromptResponse
from app.services.architecture import ArchitectureService
from app.schemas.architecture import GetArchitectureRequest, GetArchitectureResponse, UpdateArchitectureRequest


class PromptService:

    def update_architecture(request: PostPromptRequest, db: Session) -> PostPromptResponse:
        getArchitectureRequest: GetArchitectureRequest = GetArchitectureRequest(id=str(request.architecture_id))

        # get architecture
        architecture: GetArchitectureResponse = ArchitectureService.get(getArchitectureRequest, db)

        # TODO: send prompt, architecture diagram and the update existing architecture diagram
        updatedArchitecture = architecture.xml_diagram

        # update architecture request
        updateArchitectureRequest: UpdateArchitectureRequest = UpdateArchitectureRequest(xml_diagram=updatedArchitecture)

        # get the updated diagram and update the architecture diagram using the arch service
        ArchitectureService.update(str(request.architecture_id), updateArchitectureRequest, db)

        response = PostPromptResponse(xml_diagram=updatedArchitecture)
        return response
