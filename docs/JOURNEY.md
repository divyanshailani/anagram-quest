# Anagram Quest — Full Journey

## Phase 0: Concept

Goal: build a portfolio-grade system combining RL environment design, local/remote AI inference, and polished game UX.

## Phase 1: Local MLX and Inference Baseline

- Initial experiments on Apple Silicon
- FastAPI game server foundation
- Early latency and model loading constraints discovered

## Phase 2: OpenEnv Environment (Part 1)

Repository: [anagram-quest-openenv](https://github.com/divyanshailani/anagram-quest-openenv)

Delivered:
- OpenEnv reset/step semantics
- Typed Pydantic action/observation models
- Reward shaping and progression logic
- Browser-playable interface on HF Space

Key fixes:
- Session robustness in iframe contexts
- Prevented answer leakage from state
- Hardened API flow for hosted environment

## Phase 2.5: Training and Data Pipeline

- Synthetic anagram data generation
- SFT warmup + GRPO-oriented training approach
- Adapter merge and conversion path design
- Practical constraints documented for M4 vs Colab workflow

## Phase 3: Frontend Product UX (Part 2B)

Repository: [anagram-quest-frontend](https://github.com/divyanshailani/anagram-quest-frontend)

Delivered:
- Watch AI Play mode
- Terminal-like thinking feed
- Sound events and polished visual design
- PvAI route with split-screen competition

## Phase 4: Production Deployment (Part 2A)

Repository: [anagram-quest-server](https://github.com/divyanshailani/anagram-quest-server)

Delivered:
- DigitalOcean deployment with Nginx reverse proxy
- systemd managed service
- SSL and domain routing
- Vercel frontend to droplet backend integration

## Phase 5: Oracle Integration

- Oracle service integration for anagram solving
- Health checks and robustness around oracle availability

## Phase 6: Player vs AI Mode

Delivered:
- Match create/guess/next-level/status endpoints
- AI SSE stream for competitive rounds
- Human vs AI scoring and level flow

Key fixes:
- Duplicate AI scoring on reconnect
- Auto-advance timing edge cases
- Anti-cheat masking (hide AI words in PvAI)

## Phase 6.5: Stability Sprint (Mar 26-27, 2026)

Major improvements:
- Premium PvAI visual upgrade
- Banking system integration in PvAI (human + AI)
- Faster AI cadence and oracle timeout fallback behavior
- Stale-level correctness contract to prevent false negatives
- One-click rematch reliability (`starting` state)
- Match lifecycle TTL fixes
- Oracle pooling + cache for improved response consistency
- Nginx SSE hardening with dedicated route behavior
- Runtime alignment to single-worker in-memory safety model

Outcome:
- System is now stable for real usage and profile demonstration
- Architecture and operational behavior are explainable and reproducible

## Next Milestones

- Structured 10-20 user load testing with p95/p99 tracking
- Redis-backed shared state for multi-worker/multi-instance scaling
- Next GRPO iteration informed by live gameplay telemetry
- Mobile-specific competitive UX pass
