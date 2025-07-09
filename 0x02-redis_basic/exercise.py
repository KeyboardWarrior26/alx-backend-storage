#!/usr/bin/env python3
"""
This module defines a Cache class that interacts with Redis.
It allows storing data using randomly generated keys.
"""

import redis
import uuid
from typing import Union


class Cache:
    """
    Cache class for storing data in Redis with random keys.
    """

    def __init__(self) -> None:
        """
        Initialize the Cache instance by connecting to Redis and flushing the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data in Redis using a random UUID key.

        Args:
            data (str | bytes | int | float): The data to store in Redis.

        Returns:
            str: The randomly generated key under which the data was stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
