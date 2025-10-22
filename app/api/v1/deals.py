from fastapi import APIRouter, Depends, Path
from sqlmodel import Session
from app.core.db import get_session
from app.core.security import require_active
from app.domain.deals.schemas import (
    DealCreate, DealListItem, DealRead, ParticipantAdd, ParticipantRead,
    DealActionCreate, DealActionRead
)
from app.domain.deals.service import (
    create_deal, get_my_deals_view, add_participant_to_deal, get_deal_participants,
    list_actions_view, add_action_to_deal,
    accept_terms, reserve_guarantee, confirm_done, start_arbitration
)

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



@router.get("/{deal_id}/actions", response_model=list[DealActionRead])
def list_actions_ep(deal_id: int, session: Session = Depends(get_session), user=Depends(require_active)):
    return list_actions_view(session, deal_id, user.id)

@router.post("/{deal_id}/actions", response_model=DealActionRead)
def add_action_ep(
    deal_id: int,
    payload: DealActionCreate,
    session: Session = Depends(get_session),
    user=Depends(require_active),
):
    return add_action_to_deal(session, deal_id, user, payload.description)

@router.post("/{deal_id}/accept-terms")
def accept_terms_ep(deal_id: int, session: Session = Depends(get_session), user=Depends(require_active)):
    return accept_terms(session, deal_id, user)

@router.post("/{deal_id}/guarantee/reserve")
def reserve_ep(deal_id: int, session: Session = Depends(get_session), user=Depends(require_active)):
    return reserve_guarantee(session, deal_id, user)

@router.post("/{deal_id}/confirm-done")
def confirm_done_ep(deal_id: int, session: Session = Depends(get_session), user=Depends(require_active)):
    return confirm_done(session, deal_id, user)

@router.post("/{deal_id}/arbitration/start")
def start_arbitration_ep(deal_id: int, session: Session = Depends(get_session), user=Depends(require_active)):
    return start_arbitration(session, deal_id, user)
