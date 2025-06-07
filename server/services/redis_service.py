import redis
import threading


def get_redis():
  return RedisService()


def get_redis_config():
  return {
    "host": "localhost",
    "port": 6379,
    "decode_responses": True,
    "charset": "utf-8",
    "encoding": "utf-8"
  }


class RedisService:
  _instance = redis.Redis(**get_redis_config())
  _lock = threading.Lock()

  def __new__(cls, config=None):
    if cls._instance is None:
      with cls._lock:
        # Another thread could have created the instance
        # before we acquired the lock. So check that the
        # instance is still non-existent.
        if not cls._instance:
          cls._instance = super().__new__(cls, **get_redis_config())
    return cls._instance
