from fastapi import APIRouter
router = APIRouter()

@router.get("/health")
def arbitration_health():
    return {"ok": True}