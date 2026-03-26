# Repo Topology

## Why Anagram Quest is Split

The project is intentionally split by deployment/runtime concern:

1. **Environment repo** for OpenEnv and RL usage
2. **Backend runtime repo** for production game server
3. **Frontend repo** for Vercel deployment
4. **This umbrella repo** for story, architecture, and recruiter navigation

## Repositories

### 1) anagram-quest-openenv

- Purpose: RL environment and standalone gameplay foundation
- Includes: OpenEnv models, environment logic, API/web routes, docs assets
- Link: [github.com/divyanshailani/anagram-quest-openenv](https://github.com/divyanshailani/anagram-quest-openenv)

### 2) anagram-quest-server

- Purpose: Production game master backend for Watch/PvAI modes
- Includes: FastAPI APIs, SSE streams, banking logic, deployment scripts
- Link: [github.com/divyanshailani/anagram-quest-server](https://github.com/divyanshailani/anagram-quest-server)

### 3) anagram-quest-frontend

- Purpose: User-facing game application
- Includes: Next.js routes, match engine hooks, PvAI UI, sound/feedback systems
- Link: [github.com/divyanshailani/anagram-quest-frontend](https://github.com/divyanshailani/anagram-quest-frontend)

### 4) anagram-quest (this repo)

- Purpose: Portfolio-grade unified narrative and architecture index
- Includes: journey documentation, topology, deployment/scale strategy
- Link: [github.com/divyanshailani/anagram-quest](https://github.com/divyanshailani/anagram-quest)

## Integration Flow

- Frontend calls backend over HTTPS
- Backend streams AI events through SSE
- Backend calls Oracle for candidate generation
- OpenEnv repo provides core environment lineage and reward design principles

## Recommended Recruiter Path

1. Start with this repo README (big picture)
2. Open `docs/JOURNEY.md` (problem-solving depth)
3. Visit frontend + server repos (implementation depth)
4. Visit OpenEnv repo (research/RL foundation)
