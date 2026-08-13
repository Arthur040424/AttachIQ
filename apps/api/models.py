import uuid, enum
from datetime import datetime
from sqlalchemy import String, DateTime, func, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Institution(Base):
    __tablename__ = "institutions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    # server_default=func.now() tells postgres to fill in the current timestamp when a new record is created
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    users: Mapped[list["User"]] = relationship(back_populates="institution")


class UserRole(str, enum.Enum):
        COORDINATOR = "COORDINATOR"
        SUPERVISOR = "SUPERVISOR"
        STUDENT = "STUDENT"
        INSTITUTION_ADMIN = "INSTITUTION_ADMIN"


class User(Base):
        __tablename__ = "users"

        id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        institution_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institutions.id"), nullable=False)
        email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
        hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
        full_name: Mapped[str] = mapped_column(String(255), nullable=False)
        role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

        institution: Mapped["Institution"] = relationship(back_populates="users")


class Programme(Base):
       __tablename__ = "programmes"

       id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
       institution_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institutions.id"), nullable=False)
       name: Mapped[str] = mapped_column(String(255), nullable=False)
       created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

       competency_units: Mapped[list["CompetencyUnit"]] = relationship(back_populates="programme")


class CompetencyUnit(Base):
       __tablename__ = "competency_units"


       id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
       programme_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("programmes.id"), nullable=False)
       code: Mapped[str] = mapped_column(String(50), nullable=False)
       name: Mapped[str] = mapped_column(String(255), nullable=False)
       created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

       programme: Mapped["Programme"] = relationship(back_populates="competency_units")