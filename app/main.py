from fastapi import FastAPI
from app.api.v1.router import api_v1
from sqlmodel import SQLModel, Session
from app.core.db import engine
from app.domain.roles.repo import ensure_seed

# 👉 додай ці імпорти, щоб зареєструвати всі таблиці
from app.domain.roles import models as _roles_models      # noqa: F401
from app.domain.users import models as _users_models      # noqa: F401
from app.domain.wallets import models as _wallets_models  # noqa: F401
from app.domain.deposits import models as _deps_models    # noqa: F401
from app.domain.deals import models as _deals_models      # noqa: F401
from app.domain.wallets import transactions as _wtx_models# noqa: F401

app = FastAPI(title="Club Guarantees MVP")
app.include_router(api_v1, prefix="/api/v1")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        ensure_seed(s)