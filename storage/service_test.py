import unittest
import redis
from service import Service


class ServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.redis_client = redis.Redis(
            host="localhost",
            port=6379,
            password="",
            db=0
        )
        self.service = Service()
        self.service.client = self.redis_client

    def tearDown(self) -> None:
        self.redis_client.flushall()
        self.redis_client.close()

    def test_ping(self):
        response = self.service.ping()
        self.assertEqual(response, "PONG")

    def test_setUrlMapping(self):
        shorturl = "short"
        originalurl = "https://en.wikipedia.org/wiki/Python_(programming_language)"

        self.service.setUrlMapping(shorturl=shorturl, originalurl=originalurl)
        response = self.service.client.get(shorturl)
        self.assertEqual(response.decode(), originalurl)

    def test_getUrlMapping(self):
        shorturl = "short"
        originalurl = "https://en.wikipedia.org/wiki/Python_(programming_language)"

        self.service.client.set(shorturl, originalurl)
        response = self.service.getUrlMapping(shorturl=shorturl)

        self.assertEqual(response, originalurl)
