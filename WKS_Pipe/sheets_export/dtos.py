from typing import Optional
from pydantic import BaseModel


class Coordinate(BaseModel):
    X: float
    Y: float
    Step: Optional[int] = None  # TODO
