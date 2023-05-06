from fastapi import FastAPI

import config
from dto.response import InterpolationResultTo
from dto.request import InterpolationRequestTo
from interpolation import interpolation_manager
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = config.origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/interpolation")
async def interpolate(data: InterpolationRequestTo) -> InterpolationResultTo:
    return interpolation_manager.interpolate(data)
