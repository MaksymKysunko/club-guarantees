from sqlmodel import Session
from app.core.errors import bad_request, not_found, forbidden
from app.domain.users.repo import get as get_user
from .models import Deal, DealParticipant, DealAction
from app.domain.wallets.repo import get_wallet_by_user_currency
from .repo import (
    add_deal, add_participant, get_deal, is_participant, list_my_deals, list_participants,
    get_participant, list_actions, add_action, list_all_participants
)

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

def list_actions_view(session: Session, deal_id: int, current_user_id: int):
    deal = get_deal(session, deal_id)
    if not deal:
        not_found("Deal not found")
    if not is_participant(session, deal_id, current_user_id):
        forbidden("Only participants can view actions")
    return list_actions(session, deal_id)

def add_action_to_deal(session: Session, deal_id: int, actor_user, description: str):
    deal = get_deal(session, deal_id)
    if not deal:
        not_found("Deal not found")
    # додавати може учасник або admin/banker
    role_code = getattr(getattr(actor_user, "role", None), "code", None)
    if not (is_participant(session, deal_id, actor_user.id) or role_code in ("admin", "banker")):
        forbidden("Only participants or admin/banker can add actions")

    a = DealAction(deal_id=deal_id, description=description.strip(), creator_id=actor_user.id)
    return add_action(session, a)

def accept_terms(session: Session, deal_id: int, actor_user):
    deal = get_deal(session, deal_id)
    if not deal:
        not_found("Deal not found")
    p = get_participant(session, deal_id, actor_user.id)
    if not p:
        forbidden("Only participants can accept terms")
    if p.terms_accepted:
        return {"status": "unchanged"}
    p.terms_accepted = True
    session.add(p)
    session.commit()
    _maybe_update_status_after_terms(session, deal)
    return {"status": "accepted"}

def reserve_guarantee(session: Session, deal_id: int, actor_user):
    deal = get_deal(session, deal_id)
    if not deal:
        not_found("Deal not found")
    p = get_participant(session, deal_id, actor_user.id)
    if not p:
        forbidden("Only participants can reserve")
    if p.reserved:
        return {"status": "unchanged"}

    # знайдемо гаманець користувача у валюті угоди
    w = get_wallet_by_user_currency(session, actor_user.id, deal.currency)
    if not w:
        bad_request("Open a wallet in deal currency first")

    available = (w.balance or 0.0) - (w.reserved or 0.0)
    if available < deal.guarantee_total:
        bad_request("Insufficient available funds to reserve guarantee")

    # резервуємо
    w.reserved = (w.reserved or 0.0) + deal.guarantee_total
    p.reserved = True
    session.add(w)
    session.add(p)
    session.commit()

    _maybe_update_status_after_reserve(session, deal)
    return {"status": "reserved"}

def confirm_done(session: Session, deal_id: int, actor_user):
    deal = get_deal(session, deal_id)
    if not deal:
        not_found("Deal not found")
    p = get_participant(session, deal_id, actor_user.id)
    if not p:
        forbidden("Only participants can confirm")
    if p.done_confirmed:
        return {"status": "unchanged"}

    p.done_confirmed = True
    session.add(p)
    session.commit()

    _maybe_complete_and_release(session, deal)
    return {"status": "confirmed"}

def start_arbitration(session: Session, deal_id: int, actor_user):
    deal = get_deal(session, deal_id)
    if not deal:
        not_found("Deal not found")
    if not is_participant(session, deal_id, actor_user.id):
        forbidden("Only participants can start arbitration")
    if deal.status in ("completed", "cancelled"):
        bad_request("Deal is already closed")
    deal.status = "in_arbitration"
    session.add(deal)
    session.commit()
    return {"status": "in_arbitration"}

# --- helpers: автостатуси ---

def _maybe_update_status_after_terms(session: Session, deal: Deal):
    parts = list_all_participants(session, deal.id)
    if parts and all(p.terms_accepted for p in parts):
        if deal.status == "draft":
            deal.status = "terms_accepted"
            session.add(deal)
            session.commit()

def _maybe_update_status_after_reserve(session: Session, deal: Deal):
    parts = list_all_participants(session, deal.id)
    if any(p.reserved for p in parts):
        if deal.status in ("draft", "terms_accepted"):
            deal.status = "funding"
    if parts and all(p.reserved for p in parts):
        deal.status = "funded"
    session.add(deal)
    session.commit()

def _maybe_complete_and_release(session: Session, deal: Deal):
    parts = list_all_participants(session, deal.id)
    if not parts or not all(p.done_confirmed for p in parts):
        return
    # реліз гарантій для всіх, у кого reserved=True
    for p in parts:
        if not p.reserved:
            continue
        w = get_wallet_by_user_currency(session, p.user_id, deal.currency)
        if w and (w.reserved or 0.0) >= deal.guarantee_total:
            w.reserved = (w.reserved or 0.0) - deal.guarantee_total
            session.add(w)
        p.reserved = False
        session.add(p)
    deal.status = "completed"
    session.add(deal)
    session.commit()