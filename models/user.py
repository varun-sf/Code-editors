from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from models.code_file import user_codefile_association 


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    owned_files = relationship("CodeFile", back_populates="owner")  # Files owned by the user
    shared_files = relationship("CodeFile", secondary=user_codefile_association, back_populates="collaborators")  # Files shared with the user
