from sqlalchemy import Column, Integer, String
from ..db import Base


class Pokemon(Base):
    __tablename__ = "pokemon"

    id: int = Column(Integer(), primary_key=True)
    name: str = Column(String(50), nullable=False, unique=True)
    weight: float = Column(Integer(), nullable=True, unique=False)

    def __repr__(self) -> str:
        return f"<Pokemon({self.id=}, {self.name=}, {self.weight=})>"
