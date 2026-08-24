# importing every model registers it on the shared Base metadata used by create_all
from app.models.users import User
from app.models.projects import Project
from app.models.architecture import Architecture
from app.models.roadmap import Roadmap
from app.models.infrastructure_cost import InfrastructureCost
from app.models.generation import Generation
