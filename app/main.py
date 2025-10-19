from fastapi import FastAPI
from app.api.v1.router import api_v1
from sqlmodel import SQLModel
from app.core.db import engine, get_session
from app.domain.roles.repo import ensure_seed

app = FastAPI(title="Club Guarantees MVP")
app.include_router(api_v1, prefix="/api/v1")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    # seed roles
    from sqlmodel import Session
    with Session(engine) as s:
        ensure_seed(s)
