# app/models/bike.py
from datetime import date, datetime  # <-- Python-Typen

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Bike(Base):
    __tablename__ = "bikes"
    __table_args__ = (UniqueConstraint("owner_id", "frame_number", name="u_owner_frame"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    brand: Mapped[str] = mapped_column(String(120), nullable=False)
    model: Mapped[str | None] = mapped_column(String(120), nullable=True)
    color: Mapped[str | None] = mapped_column(String(60), nullable=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    frame_number: Mapped[str | None] = mapped_column(String(120), nullable=True)
    purchase_date: Mapped[date | None] = mapped_column(Date, nullable=True)  # <-- Python: date
    weight_kg: Mapped[int | None] = mapped_column(Integer, nullable=True)
    brake_type: Mapped[str | None] = mapped_column(String(60), nullable=True)
    tire_size: Mapped[str | None] = mapped_column(String(40), nullable=True)

    created_at: Mapped[datetime] = mapped_column(  # <-- Python: datetime
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    owner = relationship("User", backref="bikes")
