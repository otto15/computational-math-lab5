from typing import Callable


class InterpolationData:
    x: list[float]
    y: list[float]

    def __init__(self, x, y):
        self.x = x
        self.y = y


class InterpolationResult:
    func: str

    def __init__(self, func):
        self.func = func
