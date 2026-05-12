import redis
import json
import os
from dotenv import load_dotenv
load_dotenv()

# Connect to Redis
r = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

def save_history(session_id: str, history: list):
    """Save conversation history to Redis."""
    r.setex(
        f"session:{session_id}",
        3600,  # Expire after 1 hour
        json.dumps(history)
    )

def load_history(session_id: str) -> list:
    """Load conversation history from Redis."""
    data = r.get(f"session:{session_id}")
    if data:
        return json.loads(data)
    return []

def clear_history(session_id: str):
    """Delete conversation history from Redis."""
    r.delete(f"session:{session_id}")