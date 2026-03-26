# Project Story (Portfolio + Interview Narrative)

## One-Line Story

I built Anagram Quest as a full-stack AI game system that started as an RL-compatible environment and evolved into a production-deployed competitive PvAI product.

## Why This Project Matters

Most projects stop at either model experimentation or UI demo polish. This one demonstrates both:

- environment and reward design (OpenEnv-ready foundation)
- production backend engineering (FastAPI, SSE, reliability fixes)
- polished frontend UX (Next.js, premium gameplay feel)
- real operations discipline (Nginx, systemd, deployment hardening)

## Build Arc

1. Start with deterministic anagram environment and clean step/reset contracts.
2. Build training/data path for future GRPO iterations.
3. Build user-facing watch and PvAI modes with fast feedback loops.
4. Deploy and run in production with real users.
5. Fix reliability edge-cases until behavior becomes stable and explainable.

## Hard Problems Solved

- Reconnect-safe SSE without duplicate AI scoring.
- Human submit reliability at speed (Enter-key race conditions removed).
- Stale-level correctness during rapid transitions.
- In-memory state safety under process-model constraints.
- Proxy-level SSE buffering and timeout behavior in production.

## What Makes It Portfolio-Strong

- It is a system, not a single script.
- It has visible product quality and clear technical depth.
- It includes deployment, incidents, fixes, and scaling roadmap.
- It connects ML experimentation to user-facing value.

## How To Present In Interviews (Short)

1. "Part 1 was environment correctness and reward design."
2. "Part 2 was productization: backend SSE orchestration plus premium frontend UX."
3. "Then I solved production reliability issues one by one: reconnects, stale state, proxy buffering, and lifecycle races."
4. "Next scale step is Redis-backed shared state to unlock multi-worker and multi-instance expansion."

## Supporting Docs

- Timeline: [JOURNEY.md](JOURNEY.md)
- Production incidents/fixes: [POSTMORTEM.md](POSTMORTEM.md)
- Deployment and scale path: [DEPLOYMENT_AND_SCALE.md](DEPLOYMENT_AND_SCALE.md)
- Direct code pointers: [CODE_MAP.md](CODE_MAP.md)
