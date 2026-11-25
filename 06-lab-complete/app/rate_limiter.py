"""
Rate limiting (tiêu chí 7).

Sliding window 60 giây cho mỗi API key, state lưu trong Redis sorted set.
Dùng Lua script để kiểm tra + ghi nhận nguyên tử (atomic) giữa nhiều worker.
"""
import time
import uuid

from fastapi import HTTPException

from app.config import settings
from app.redis_client import r

WINDOW_SECONDS = 60

# Trả về 1 nếu cho phép, 0 nếu vượt giới hạn.
_SLIDING_WINDOW_LUA = """
local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])
local member = ARGV[4]

redis.call('ZREMRANGEBYSCORE', key, 0, now - window)
local count = redis.call('ZCARD', key)
if count >= limit then
    return 0
end
redis.call('ZADD', key, now, member)
redis.call('EXPIRE', key, math.ceil(window))
return 1
"""

_check_and_add = r.register_script(_SLIDING_WINDOW_LUA)


def check_rate_limit(key: str) -> None:
    """Vượt RATE_LIMIT_PER_MINUTE request / 60 giây → HTTP 429."""
    allowed = _check_and_add(
        keys=[f"ratelimit:{key}"],
        args=[time.time(), WINDOW_SECONDS, settings.rate_limit_per_minute, uuid.uuid4().hex],
    )
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={"Retry-After": str(WINDOW_SECONDS)},
        )
