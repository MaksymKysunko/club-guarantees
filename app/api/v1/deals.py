from fastapi import APIRouter, Depends, Path
from sqlmodel import Session
from app.core.db import get_session
from app.core.security import require_active
from app.domain.deals.schemas import DealCreate, DealListItem, DealRead, ParticipantAdd, ParticipantRead
from app.domain.deals.service import create_deal, get_my_deals_view, add_participant_to_deal, get_deal_participants

router = APIRouter()

@router.get("/", response_model=list[DealListItem])
def list_my_deals_ep(session: Session = Depends(get_session), user=Depends(require_active)):
    return get_my_deals_view(session, user.id)

@router.post("/", response_model=DealRead)
def create_deal_ep(payload: DealCreate, session: Session = Depends(get_session), user=Depends(require_active)):
    return create_deal(session, user, payload.title, payload.currency, payload.guarantee_total)

@router.post("/{deal_id}/participants", response_model=ParticipantRead)
def add_participant_ep(
    payload: ParticipantAdd,
    deal_id: int = Path(..., ge=1),
    session: Session = Depends(get_session),
    user=Depends(require_active),
):
    return add_participant_to_deal(session, deal_id, user, payload.user_id)

@router.get("/{deal_id}/participants", response_model=list[ParticipantRead])
def list_participants_ep(deal_id: int, session: Session = Depends(get_session), user=Depends(require_active)):
    return get_deal_participants(session, deal_id)
