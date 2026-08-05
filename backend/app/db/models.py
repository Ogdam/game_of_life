from datetime import datetime

from sqlalchemy import Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

DEFAULT_GRID_SIZE = 90


class SessionModel(Base):  # pylint: disable=too-few-public-methods
    __tablename__ = "sessions"

    client_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    width: Mapped[int] = mapped_column(
        Integer, nullable=False, default=DEFAULT_GRID_SIZE
    )
    height: Mapped[int] = mapped_column(
        Integer, nullable=False, default=DEFAULT_GRID_SIZE
    )
    state: Mapped[str] = mapped_column(String(16), nullable=False, default="pause")
    speed: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    tick: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    grid: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),  # pylint: disable=not-callable
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),  # pylint: disable=not-callable
        onupdate=func.now(),  # pylint: disable=not-callable
        nullable=False,
    )
