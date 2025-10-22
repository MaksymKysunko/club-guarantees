from sqlmodel import Session
from app.core.errors import bad_request, not_found, forbidden
from app.domain.users.repo import get as get_user
from .models import Deal, DealParticipant
from .repo import add_deal, add_participant, get_deal, is_participant, list_my_deals, list_participants

def create_deal(session: Session, actor_user, title: str, currency: str, guarantee_total: float) -> Deal:
    cur = currency.upper().strip()
    if not title or not cur or guarantee_total <= 0:
        bad_request("title, currency and positive guarantee_total are required")
    d = Deal(title=title.strip(), currency=cur, guarantee_total=guarantee_total, status="draft")
    d = add_deal(session, d)
    # автор стає першим учасником
    add_participant(session, DealParticipant(deal_id=d.id, user_id=actor_user.id))
    return d

def assert_can_modify_participants(session: Session, deal: Deal, actor_user):
    # може додавати учасників: адміністратор/банкір або будь-хто з УЧАСНИКІВ цієї угоди
    role_code = getattr(getattr(actor_user, "role", None), "code", None)
    if role_code in ("admin", "banker"):
        return
    if is_participant(session, deal.id, actor_user.id):
        return
    forbidden("Only a deal participant or admin/banker can modify participants")

def add_participant_to_deal(session: Session, deal_id: int, actor_user, target_user_id: int):
    deal = get_deal(session, deal_id)
    if not deal:
        not_found("Deal not found")
    assert_can_modify_participants(session, deal, actor_user)

    u = get_user(session, target_user_id)
    if not u or not u.is_active:
        bad_request("Target user not found or not active")

    if is_participant(session, deal_id, target_user_id):
        bad_request("User is already a participant of this deal")

    return add_participant(session, DealParticipant(deal_id=deal_id, user_id=target_user_id))

def get_my_deals_view(session: Session, current_user_id: int):
    rows = list_my_deals(session, current_user_id)
    return [
        {
            "id": d.id,
            "title": d.title,
            "currency": d.currency,
            "guarantee_total": d.guarantee_total,
            "status": d.status,
            "created_at": d.created_at,
            "participants_count": int(cnt or 0),
        }
        for (d, cnt) in rows
    ]

def get_deal_participants(session: Session, deal_id: int):
    return list_participants(session, deal_id)
