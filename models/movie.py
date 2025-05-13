from bd.database import Base
from sqlalchemy import Column, Integer, String


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    director = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Movie(title={self.title}, release_date={self.release_date}, genre={self.genre})>"