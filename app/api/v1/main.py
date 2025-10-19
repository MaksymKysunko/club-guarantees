from fastapi import FastAPI
from app.api.v1.router import api_v1

app = FastAPI(title="Club Guarantees MVP")
app.include_router(api_v1, prefix="/api/v1")
