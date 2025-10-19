from fastapi import APIRouter
router = APIRouter()

@router.get("/health")
def wallets_health():
    return {"ok": True}