from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.config.database import Base


class Generation(Base):
    """One pipeline run: analyze -> architecture -> critique loop -> roadmap -> costs."""

    __tablename__ = "generations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), nullable=False)
    architecture_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("architectures.id"), nullable=True)
    status: Mapped[str] = mapped_column(String, default="queued")  # queued | running | completed | failed
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    # which model served each pipeline step, tokens and estimated spend
    model_usage: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    total_cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
