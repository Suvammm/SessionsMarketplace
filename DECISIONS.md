# Decision 1: Booking concurrency strategy

## Problem

Simultaneous requests must not exceed capacity.

## Options considered

1. Check remaining seats in React.
2. Count then create without locking.
3. Lock the session row in a PostgreSQL transaction.

## Choice

Option 3: `atomic()` plus `select_for_update()` locks the session while ACTIVE bookings are counted and created.

## Trade-off

Contending requests serialize briefly. Frontend seat counts are only UX; application-only checks race. PostgreSQL protects the duplicate-active invariant with a conditional unique constraint; the transaction protects capacity and start-time checks.

# Decision 2: Duplicate booking protection

## Problem

One user must not hold two active reservations for a session.

## Options considered

1. Application `exists()` check only.
2. Unconditional unique pair.
3. Conditional unique constraint for ACTIVE status.

## Choice

Option 3 preserves booking history after cancellation while making the invariant database-enforced.

## Trade-off

It relies on PostgreSQL partial-index support, which matches the production database.

# Decision 3: Authorization and interface

## Problem

Creator controls must remain secure even if clients are modified.

## Options considered

1. Hide buttons only.
2. Backend role and ownership permissions with matching UI.
3. Separate creator service.

## Choice

Option 2 keeps the system compact: `IsCreator` gates creator endpoints and owner checks gate mutations.

## Trade-off

The UI still needs to handle 403 responses, but clients cannot bypass the API checks.
