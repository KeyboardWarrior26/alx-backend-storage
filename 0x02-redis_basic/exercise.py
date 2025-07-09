#!/usr/bin/env python3
"""
This module defines a Cache class that interacts with Redis.
It allows storing data using randomly generated keys,
retrieving them with optional conversion,
and counting method calls using a decorator.
"""

import redis
import uuid
from typing import Union, Callable, Optional, TypeVar
from functools import wraps

F = TypeVar("F", bound=Callable)


def count_calls(method: F) -> F:
    """
    Decorator to count how many times a method is called,
    using Redis with the method's qualified name as key.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper  # type: ignore


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

    @count_calls
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

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis using the given key and optionally
        apply a transformation function.

        Args:
            key (str): The Redis key to look up.
            fn (Callable, optional): Function to convert data type.

        Returns:
            The stored value (optionally transformed), or None if the key does not exist.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a UTF-8 string from Redis.

        Args:
            key (str): The Redis key.

        Returns:
            Optional[str]: The decoded string or None if key not found.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer from Redis.

        Args:
            key (str): The Redis key.

        Returns:
            Optional[int]: The integer value or None if key not found.
        """
        return self.get(key, fn=int)

