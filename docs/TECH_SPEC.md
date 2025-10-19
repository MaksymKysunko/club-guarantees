# Club Guarantees  Технічне завдання (MVP)

## Цілі MVP
- Депозити учасників (ручний апрув банкіром).
- Угода: умови, учасники, чекліст дій.
- Прийняття умов усіма учасниками.
- Резервація гарантії через блокування депозиту (holds).
- Завершення або арбітраж.

## Ролі
- member  учасник клубу
- banker  касир/арбітр (апрув депозитів, рішення по арбітражу)

## Сутності та інваріанти
- Users(id, email, nick, role, created_at)
- Wallets(id, user_idUsers.id, currency, account_code, created_at)
- DepositRequests(id, user_id, currency, amount, status[pending|approved|rejected], note, created_at, approved_at)
- Balances(id, user_id, currency, amount)
- Deals(id, title, currency, guarantee_total, status[draft|terms_accepted|funding|funded|in_arbitration|completed|cancelled], created_at)
- DealParticipants(id, deal_idDeals.id, user_idUsers.id, terms_accepted, done_confirmed)
- DealActions(id, deal_idDeals.id, description, creator_idUsers.id)
- Holds(id, user_idUsers.id, deal_idDeals.id, currency, amount, status[active|released|confiscated], created_at, released_at)

Інваріанти:
- available = balance.amount  sum(active holds.amount).
- Арбітраж дозволений лише коли всі учасники мають активні hold'и на гарантійну суму.
- Завершення: всі учасники підтвердили виконання  всі hold'и release.

## Стани угоди
draft  terms_accepted  funding  funded  (in_arbitration | completed | cancelled)
