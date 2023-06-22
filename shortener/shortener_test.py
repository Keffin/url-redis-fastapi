import unittest
import hashlib
import base58
import shortener


class ShortenerTest(unittest.TestCase):
    def test_sha256Of(self):
        input_str = "Hello, World!"
        expected_hash = hashlib.sha256(input_str.encode()).digest()

        self.assertEqual(shortener.sha256Of(input_str), expected_hash)

    def test_baseEncoded(self):
        input_bytes = b"\x00\x01\x02\x03\x04\x05"
        expected_encoded = base58.b58encode(input_bytes).decode()
        self.assertEqual(shortener.baseEncoded(input_bytes), expected_encoded)

    def test_createShortLink(self):
        original_url = "https://example.com"

        url_hash_bytes = hashlib.sha256(original_url.encode()).digest()
        random_num = int.from_bytes(url_hash_bytes, byteorder="big")
        end_result_str = base58.b58encode(bytes(str(random_num), "utf-8")).decode()
        expected_short_link = end_result_str[:8]

        self.assertEqual(shortener.createShortLink(original_url), expected_short_link)
