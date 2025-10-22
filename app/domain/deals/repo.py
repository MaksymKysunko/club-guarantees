from typing import List, Optional, Tuple
from sqlmodel import Session, select, func
from .models import Deal, DealParticipant

def add_deal(session: Session, d: Deal) -> Deal:
    session.add(d)
    session.commit()
    session.refresh(d)
    return d

def add_participant(session: Session, p: DealParticipant) -> DealParticipant:
    session.add(p)
    session.commit()
    session.refresh(p)
    return p

def get_deal(session: Session, deal_id: int) -> Optional[Deal]:
    return session.get(Deal, deal_id)

def is_participant(session: Session, deal_id: int, user_id: int) -> bool:
    stmt = select(DealParticipant).where(
        DealParticipant.deal_id == deal_id,
        DealParticipant.user_id == user_id
    )
    return session.exec(stmt).first() is not None

def list_my_deals(session: Session, user_id: int) -> List[Tuple[Deal, int]]:
    # угоди, де я учасник, + підрахунок учасників
    my_deals = select(DealParticipant.deal_id).where(DealParticipant.user_id == user_id)
    stmt = (
        select(Deal, func.count(DealParticipant.id))
        .where(Deal.id.in_(my_deals))
        .join(DealParticipant, DealParticipant.deal_id == Deal.id, isouter=True)
        .group_by(Deal.id)
        .order_by(Deal.created_at.desc())
    )
    return session.exec(stmt).all()

def list_participants(session: Session, deal_id: int) -> List[DealParticipant]:
    stmt = select(DealParticipant).where(DealParticipant.deal_id == deal_id).order_by(DealParticipant.id)
    return session.exec(stmt).all()
