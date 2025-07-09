#!/usr/bin/env python3
"""
This module defines a Cache class that interacts with Redis.
It allows storing data using randomly generated keys,
retrieving them with optional conversion,
and tracking method calls and histories.
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


def call_history(method: F) -> F:
    """
    Decorator to store the history of inputs and outputs for a method in Redis.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))

        return output
    return wrapper  # type: ignore


def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function.
    Prints how many times it was called and the inputs/outputs for each call.
    """
    redis_client = redis.Redis()
    method_name = method.__qualname__

    # Get call count
    count = redis_client.get(method_name)
    count = int(count) if count else 0
    print(f"{method_name} was called {count} times:")

    # Fetch and print inputs and outputs
    inputs = redis_client.lrange(f"{method_name}:inputs", 0, -1)
    outputs = redis_client.lrange(f"{method_name}:outputs", 0, -1)

    for inp, out in zip(inputs, outputs):
        print(f"{method_name}(*{inp.decode('utf-8')}) -> {out.decode('utf-8')}")


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
    @call_history
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
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer from Redis.
        """
        return self.get(key, fn=int)

