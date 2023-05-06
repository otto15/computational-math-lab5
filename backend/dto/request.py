from pydantic import BaseModel


class PointTo(BaseModel):
    x: float
    y: float


class InterpolationRequestTo(BaseModel):
    points: list[PointTo]
