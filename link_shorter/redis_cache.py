import json

import redis

CACHE_TTL = 3600

class RedisCache:
    def __init__(self, host="redis", port=6379, db=1):
        self.client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def connect(self):
        try:
            self.client.ping()
            print("Redis подключен успешно")
        except redis.ConnectionError as e:
            print(f"Ошибка подключения к Redis: {e}")

    def set_url(self, hash, data):
        self.client.setex(hash, CACHE_TTL, json.dumps(data))

    def get_url(self, hash):
        print("Чекаю Redis", flush=True)
        data = self.client.get(hash)
        print(data)
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return None
        return None

    def delete_url(self, hash):
        self.client.delete(hash)


redis_cache = RedisCache()
