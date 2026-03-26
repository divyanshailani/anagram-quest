# Production Postmortem (Key Bugs and Fixes)

This document captures the highest-impact failures encountered during productionization and the exact fixes applied.

## 1) AI Duplicate Scoring After SSE Reconnect

- Symptom: AI earned duplicate points for already-found words after stream reconnect.
- Root cause: new generator state was being recreated on reconnect.
- Fix: persisted oracle generator and `ai_found` state in active match object.
- Impact: removed score inflation and restored fair max-score boundaries.

## 2) Enter Key Sometimes Did Not Register Human Guess

- Symptom: valid word entered, but submit occasionally dropped.
- Root cause: frontend race between submit lock state and async request lifecycle.
- Fix: hardened submit path in match engine; improved pending/submitting guards.
- Impact: reliable registration for rapid typing gameplay.

## 3) Correct Word Marked Wrong During Level Transition

- Symptom: valid guess near boundary was rejected.
- Root cause: request reached backend after level rolled forward.
- Fix: stale-level contract between frontend and backend; stale requests ignored safely.
- Impact: eliminated false negatives at fast transition edges.

## 4) Rematch Needed Double Click

- Symptom: restart action surfaced mode menu again or required second click.
- Root cause: race in client state where match was not yet fully in start-ready phase.
- Fix: explicit `starting` state and one-click rematch flow.
- Impact: clean end-to-end restart UX.

## 5) Active Match Expired Mid-Session

- Symptom: ongoing PvAI games could disappear (`match not found`) under pressure.
- Root cause: GC/TTL tuning too aggressive for real play duration.
- Fix: match lifecycle TTL and cleanup logic adjusted for active sessions.
- Impact: lower session drop rate and stronger continuity.

## 6) AI Stream Felt Slow or Stalled in PvAI

- Symptom: AI panel lagged despite working well in watch mode.
- Root cause: pacing choices and timeout behavior were not tuned for competitive mode.
- Fix: faster candidate cadence, timeout fallback behavior, and stream resilience updates.
- Impact: smoother real-time PvAI competition feel.

## 7) SSE Buffered by Proxy

- Symptom: backend produced events, but frontend received them in delayed chunks.
- Root cause: default proxy buffering/timeouts not SSE-optimized.
- Fix: Nginx SSE hardening (`proxy_buffering off`, `X-Accel-Buffering no`, longer timeouts).
- Impact: low-latency event delivery for long-running streams.

## 8) Multi-Worker In-Memory State Inconsistency

- Symptom: inconsistent match state when requests hit different workers.
- Root cause: active match state is in-memory and process-local.
- Fix: runtime alignment to `--workers 1` until shared state store is added.
- Impact: correctness-first operation with predictable behavior.

## 9) Oracle Latency Spikes Under Repeated Calls

- Symptom: uneven response times and intermittent UX jitter.
- Root cause: repeated uncached calls and client setup overhead.
- Fix: Oracle client pooling plus bounded response cache with TTL.
- Impact: better consistency and lower backend overhead.

## Operational Result

By March 27, 2026, the system moved from fragile prototype behavior to stable profile-grade operation with clear scaling next steps.
