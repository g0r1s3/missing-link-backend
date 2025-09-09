from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, String, Integer, Boolean, ForeignKey, Numeric, Text, func
from app.db.base import Base

class Maintenance(Base):
    __tablename__ = "maintenances"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    bike_id: Mapped[int] = mapped_column(ForeignKey("bikes.id", ondelete="CASCADE"), nullable=False, index=True)

    performed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)  # Zeitpunkt
    is_external: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)        # extern vs. selbst
    description: Mapped[str | None] = mapped_column(Text, nullable=True)                    # Beschreibung
    vendor: Mapped[str | None] = mapped_column(String(200), nullable=True)                  # Firma/Ort
    cost: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)              # Kosten

    # optionale, nützliche Felder
    mileage_km: Mapped[int | None] = mapped_column(Integer, nullable=True)                  # gefahrene km beim Service
    duration_min: Mapped[int | None] = mapped_column(Integer, nullable=True)                # Dauer
    warranty: Mapped[bool | None] = mapped_column(Boolean, nullable=True)                   # Garantie-/Gewährleistungsfall?

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    bike = relationship("Bike", backref="maintenances")
