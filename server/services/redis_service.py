import redis
import threading
import json


def get_instance():
  return RedisService()


def get_redis_config():
  return {
    "host": "127.0.0.1",
    "port": 6379,
    "db": 0,
    "decode_responses": True,
  }


class RedisService:
  _instance = None
  _redis = redis.Redis(**get_redis_config())
  _lock = threading.Lock()

  def __new__(cls, config=None):
    if cls._instance is None:
      with cls._lock:
        # Another thread could have created the instance
        # before we acquired the lock. So check that the
        # instance is still non-existent.
        if not cls._instance:
          cls._instance = super().__new__(cls)
    return cls._instance

  def get_json_dict(self, key: str) -> dict | None:
    with self._lock:
      value = self._redis.get(key)
      return json.loads(value) if value else None

  def set_json_dict(self, key, value):
    with self._lock:
      self._redis.set(key, json.dumps(value))

