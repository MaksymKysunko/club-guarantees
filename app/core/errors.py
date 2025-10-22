from fastapi import HTTPException

def bad_request(msg: str) -> None:
    raise HTTPException(status_code=400, detail=msg)

def not_found(msg: str) -> None:
    raise HTTPException(status_code=404, detail=msg)

def forbidden(msg: str) -> None:
    raise HTTPException(status_code=403, detail=msg)