#!/usr/bin/env python3
""" Test web cache """

from web import get_page
import time

url = "http://slowwly.robertomurray.co.uk/delay/3000/url/http://example.com"

print("First fetch (should be slow):")
print(get_page(url))  # Takes ~3 seconds

print("\nSecond fetch (should be instant):")
print(get_page(url))  # Cached

print("\nWaiting for cache to expire...")
time.sleep(11)

print("\nThird fetch (slow again):")
print(get_page(url))  # Cached expired, fetches again

