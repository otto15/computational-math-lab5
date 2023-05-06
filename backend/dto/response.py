from pydantic import BaseModel


class InterpolationResultTo(BaseModel):
    lagrange: str
    newton: str
