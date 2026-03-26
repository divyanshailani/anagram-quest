# Code Map (Where To Read Actual Implementation)

This file is the fast path for anyone reviewing real code behind the Anagram Quest system.

## 1) Environment Foundation (Part 1)

Repository: [anagram-quest-openenv](https://github.com/divyanshailani/anagram-quest-openenv)

- Environment dynamics and rewards: [server/word_guessing_env_environment.py](https://github.com/divyanshailani/anagram-quest-openenv/blob/main/server/word_guessing_env_environment.py)
- Environment API host: [server/app.py](https://github.com/divyanshailani/anagram-quest-openenv/blob/main/server/app.py)
- Data models and contracts: [models.py](https://github.com/divyanshailani/anagram-quest-openenv/blob/main/models.py)
- OpenEnv client helper: [client.py](https://github.com/divyanshailani/anagram-quest-openenv/blob/main/client.py)

## 2) Production Backend (Part 2A)

Repository: [anagram-quest-server](https://github.com/divyanshailani/anagram-quest-server)

- Main game runtime (watch + PvAI + SSE + banking): [main.py](https://github.com/divyanshailani/anagram-quest-server/blob/main/main.py)
- Deployment automation to DigitalOcean: [deploy_do.sh](https://github.com/divyanshailani/anagram-quest-server/blob/main/deploy_do.sh)
- Production tuning notes (SSE + workers): [PROD_TUNING.md](https://github.com/divyanshailani/anagram-quest-server/blob/main/PROD_TUNING.md)
- Runtime dependencies: [requirements.txt](https://github.com/divyanshailani/anagram-quest-server/blob/main/requirements.txt)

## 3) Frontend Product (Part 2B)

Repository: [anagram-quest-frontend](https://github.com/divyanshailani/anagram-quest-frontend)

- Landing experience and mode shell: [app/page.js](https://github.com/divyanshailani/anagram-quest-frontend/blob/main/app/page.js)
- PvAI route and orchestration UI: [app/vs/page.js](https://github.com/divyanshailani/anagram-quest-frontend/blob/main/app/vs/page.js)
- Match engine state machine: [app/hooks/useMatchEngine.js](https://github.com/divyanshailani/anagram-quest-frontend/blob/main/app/hooks/useMatchEngine.js)
- Watch stream lifecycle hook: [app/hooks/useGameStream.js](https://github.com/divyanshailani/anagram-quest-frontend/blob/main/app/hooks/useGameStream.js)
- Audio event hook: [app/hooks/useSoundFX.js](https://github.com/divyanshailani/anagram-quest-frontend/blob/main/app/hooks/useSoundFX.js)
- PvAI human panel: [app/components/PlayerArena.js](https://github.com/divyanshailani/anagram-quest-frontend/blob/main/app/components/PlayerArena.js)
- PvAI AI panel: [app/components/AIArena.js](https://github.com/divyanshailani/anagram-quest-frontend/blob/main/app/components/AIArena.js)
- Banking UI in match mode: [app/components/MatchBankPanel.js](https://github.com/divyanshailani/anagram-quest-frontend/blob/main/app/components/MatchBankPanel.js)
- Banking UI in watch mode: [app/components/BankPanel.js](https://github.com/divyanshailani/anagram-quest-frontend/blob/main/app/components/BankPanel.js)

## 4) Cross-Repo Request Flow

1. User interacts with frontend (`app/vs/page.js`, `useMatchEngine.js`).
2. Frontend calls backend match endpoints in `main.py`.
3. Backend streams AI events over SSE to frontend (`AIArena.js`, stream handlers).
4. Backend calls Oracle and applies banking + scoring rules.
5. State and results are reflected back in frontend panels and score bars.

## 5) What To Read First (Reviewer Shortcut)

1. [main.py](https://github.com/divyanshailani/anagram-quest-server/blob/main/main.py)
2. [app/hooks/useMatchEngine.js](https://github.com/divyanshailani/anagram-quest-frontend/blob/main/app/hooks/useMatchEngine.js)
3. [app/vs/page.js](https://github.com/divyanshailani/anagram-quest-frontend/blob/main/app/vs/page.js)
4. [server/word_guessing_env_environment.py](https://github.com/divyanshailani/anagram-quest-openenv/blob/main/server/word_guessing_env_environment.py)
