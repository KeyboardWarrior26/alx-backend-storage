#!/usr/bin/env python3
"""
This module implements an expiring web cache and access tracker using Redis.
"""

import redis
import requests
from typing import Callable
from functools import wraps

# Redis client (shared across all functions)
redis_client = redis.Redis()


def count_url_access(method: Callable) -> Callable:
    """
    Decorator to count how many times a URL has been accessed.
    Stores count in Redis using key 'count:{url}'.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        redis_client.incr(f"count:{url}")
        return method(url)
    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL with caching.
    If the page is cached, return it.
    Otherwise, fetch it using requests, store it in Redis with a 10-second expiration.

    Args:
        url (str): The URL to fetch

    Returns:
        str: HTML content of the URL
    """
    cached = redis_client.get(url)
    if cached:
        return cached.decode('utf-8')

    # Not cached, make HTTP request
    response = requests.get(url)
    html = response.text

    # Cache the result for 10 seconds
    redis_client.setex(url, 10, html)

    return html
