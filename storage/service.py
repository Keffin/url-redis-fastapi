import redis
from fastapi import HTTPException

CACHE_DURATION = 3600


class Service:
    client: redis.Redis

    def __init__(self):
        self.client = redis.Redis(
            host="localhost",
            port=6379,
            password="",
            db=0
        )

    def ping(self):
        response = "PONG" if self.client.ping() else "Something went wrong"
        print("Redis started, pong message: " + response)
        return response

    def setUrlMapping(self, shorturl: str, originalurl: str):
        response = self.client.set(shorturl, originalurl)
        if not response:
            raise HTTPException(status_code=500, detail="Something went wrong.")

    def getUrlMapping(self, shorturl: str) -> str:
        response: bytes = self.client.get(shorturl)
        return response.decode()


storeService = Service()
storeService.ping()
