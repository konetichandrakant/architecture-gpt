from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()

class Users(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    name: Mapped[String] = mapped_column(String)
    email: Mapped[String] = mapped_column(String)
    password: Mapped[String] = mapped_column(String)