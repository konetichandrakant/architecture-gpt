from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()

class Architecture(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    xml_diagram: Mapped[str] = mapped_column(String)