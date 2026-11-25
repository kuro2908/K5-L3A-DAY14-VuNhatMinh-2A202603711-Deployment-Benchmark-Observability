"""
Kết nối Redis dùng chung cho rate limiter và cost guard.

- App vẫn khởi động được khi Redis chưa sẵn sàng: không ping lúc import.
- redis_healthy() dùng cho GET /ready.
"""
import logging

import redis

from app.config import settings

logger = logging.getLogger(__name__)

r = redis.from_url(
    settings.redis_url,
    decode_responses=True,
    socket_connect_timeout=1,
    socket_timeout=1,
    health_check_interval=30,
)


def redis_healthy() -> bool:
    """Ping Redis; lỗi kết nối / timeout → False."""
    try:
        return bool(r.ping())
    except Exception as exc:  # redis.RedisError, OSError, timeout...
        logger.warning("redis_unhealthy", extra={"error": str(exc)})
        return False
