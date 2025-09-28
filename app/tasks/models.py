# модели для задач
from sqlalchemy import Column, Integer, String, DateTime, Text, func
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(80), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False, index=True)
    status = Column(String(20), nullable=False, default="Новая")
    priority = Column(String(20), nullable=False, default="Medium")
    location_id = Column(String(50), nullable=False)

    created_by = Column(String(50), nullable=False)
    assigned_to = Column(String(50), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # ссылка на файл
    attachments = Column(String(500), nullable=True)



