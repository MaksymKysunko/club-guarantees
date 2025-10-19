from fastapi import APIRouter
router = APIRouter()

@router.get("/health")
def deposits_health():
    return {"ok": True}