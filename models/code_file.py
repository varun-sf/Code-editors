from sqlalchemy import Column, Integer, String, ForeignKey, Text, Table, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# Association table for many-to-many relationship between Users and CodeFiles
user_codefile_association = Table(
    "user_codefile",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("codefile_id", Integer, ForeignKey("codefiles.id"))
)

class CodeFile(Base):
    __tablename__ = "codefiles"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    content = Column(Text, default="")  # Stores the code content
    owner_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="owned_files")
    collaborators = relationship("User", secondary=user_codefile_association, back_populates="shared_files")
