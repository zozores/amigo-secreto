from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from database import Base

class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    token = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    match_id = Column(Integer, ForeignKey("participants.id"), nullable=True)

    match = relationship("Participant", remote_side=[id], backref="matched_by")
