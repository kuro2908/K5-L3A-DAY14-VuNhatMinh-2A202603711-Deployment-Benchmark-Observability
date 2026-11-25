# Deployment — Part 3

- **Nền tảng:** Render (Web Service, runtime Docker) + Render Key Value (Redis)
- **Public URL:** https://k5-l3a-day14-vunhatminh-2a202603711.onrender.com
- **Root Directory:** `06-lab-complete` · **Dockerfile:** `./Dockerfile` · **Health check:** `/health`
- **Biến môi trường (đặt trên Render, không ghi trong code):** `AGENT_API_KEY`, `REDIS_URL` (Internal Key Value URL), `ENVIRONMENT`, `RATE_LIMIT_PER_MINUTE`, `DAILY_BUDGET_USD`. `PORT` do Render cấp.

## Kết quả 4 lệnh tự kiểm (CP6)

| Lệnh | Kết quả |
|---|---|
| `GET /health` | 200 |
| `GET /ready` | 200 |
| `POST /ask` không key | 401 |
| `POST /ask` có key | 200 |

Ảnh minh chứng: `screenshots/part3_render_health.jpg`, `part3_render_ready.jpg`, `part3_render_curl_results.txt`.
