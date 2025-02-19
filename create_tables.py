from database import Base, engine
import models.user

Base.metadata.create_all(bind=engine)
