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

## Проведення та кореспондентський гаманець Клубу (Wallet Ledger — дані)

### 1) Кореспондентський гаманець Клубу
- Кореспондентський рахунок Клубу — **звичайний Wallet**, власник — користувач з роллю **banker**.
- Будь-яка транзакція гаманця має посилатись на кореспондента: `corresponding_wallet_id` (**NOT NULL**, FK → wallet.id).
- Перед першим депозитом мають існувати:
  - користувач-банкір,
  - клубний гаманець у відповідній валюті.

### 2) Форма рядка транзакції (узгоджена)
- `wallet_id` — гаманець, **чий стан змінюється**.
- `currency` — код системи/криптовалюти (для рядка).
- `amount_posted` — фактичний рух (±) впливає на **balance**.
- `amount_reserved` — блокування (±) впливає на **reserved**.
- `corresponding_wallet_id` — кореспондентський гаманець (NOT NULL).
- `deal_id` — якщо операція пов’язана з угодою (NOT NULL для резерв/реліз/конфіскація).
- `created_at`, `changed_at`.

> Правило знаків:  
> `amount_posted > 0` — приплив на `wallet_id`; `< 0` — відтік.  
> `amount_reserved > 0` — блок; `< 0` — розблок/зменшення блоку.

### 3) Мінімальні проведення (без логіки, лише дані)
**Депозит учасника (double-entry)**  
- Рядок на **гаманці учасника**: `amount_posted = +X`, `corresponding_wallet_id = club_wallet`.  
- Рядок на **клубному гаманці**: `amount_posted = +X`, `corresponding_wallet_id = member_wallet`.

**Резерв під угоду**  
- Рядок на **гаманці учасника**: `amount_reserved = +S`, `deal_id = …`, `corresponding_wallet_id = club_wallet`.  
- Дзеркальний резерв на клубному гаманці — **не вимагається** в MVP.

**Реліз резерву**  
- Рядок на **гаманці учасника**: `amount_reserved = -S`, `deal_id = …`, `corresponding_wallet_id = club_wallet`.

**Конфіскація (арбітраж)**  
- На **винному**: `amount_reserved = -C`, `deal_id = …`, `corresponding_wallet_id = club_wallet`.  
- На **бенефіціарі**: окремий **депозитний** рядок `amount_posted = +C`, `corresponding_wallet_id = club_wallet`.

> Усі пов’язані рядки однієї операції мають створюватись в **одній БД-транзакції**.

