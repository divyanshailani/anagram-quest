# Deployment and Scale Notes

## Current Production Stack

- Frontend: Vercel (Next.js)
- Backend: DigitalOcean droplet (FastAPI + Uvicorn + Nginx + systemd)
- Domain: `anagram-quest.mooo.com`
- Oracle: Hugging Face Space endpoint

## Stability Controls Applied

- SSE-specific Nginx route tuning:
  - `proxy_buffering off`
  - `X-Accel-Buffering no`
  - `proxy_read_timeout 3600s`
  - `proxy_send_timeout 3600s`
- Uvicorn execution aligned with in-memory match state:
  - `--workers 1 --timeout-keep-alive 75`
- Backend resilience upgrades:
  - Oracle client pooling
  - Oracle response cache with TTL and cap
  - Stale-level request handling
  - Match TTL/GC tuning

## Why `workers=1` Right Now

Current match state is maintained in-process. With multiple workers, requests for one match can hit different processes and cause inconsistency (`match not found`, divergent state, race bugs).

Scale-up path:
1. Move match/session state to Redis or database
2. Make backend stateless per worker
3. Increase workers / horizontal instances

## 10-20 User Target Guidance

Given current architecture + hardening:
- ~10 concurrent users should be stable
- ~20 can be stable depending on oracle latency and network jitter

For predictable 20+ behavior:
- Add Redis for shared state
- Add centralized cache layer
- Add load testing with thresholds and alerts

## Suggested Load Test KPIs

- SSE disconnect rate per session
- Match completion success rate
- p95/p99 latency for `/match/{id}/guess`
- oracle timeout fallback frequency
- CPU and memory usage during peak windows

## Operational Commands

```bash
# Backend status
sudo systemctl status anagram-quest --no-pager

# Live logs
journalctl -u anagram-quest -f

# Health check
curl -sS https://anagram-quest.mooo.com/health

# Validate nginx config
sudo nginx -t && sudo systemctl reload nginx
```
