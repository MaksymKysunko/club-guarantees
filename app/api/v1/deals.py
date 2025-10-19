from fastapi import APIRouter
router = APIRouter()

@router.get("/health")
def deals_health():
    return {"ok": True}