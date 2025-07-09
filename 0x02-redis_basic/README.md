# 0x02. Redis basic

## Description

This project introduces the basics of using **Redis** in Python. Redis is an in-memory data structure store, often used as a database, cache, or message broker. This project focuses on using Redis as a key-value store and simple caching layer via Python.

---

## Learning Objectives

- How to use Redis for basic operations
- How to use Redis as a simple cache
- How to interact with Redis using Python and the `redis` library

---

## Requirements

- Ubuntu 18.04 LTS
- Python 3.7
- Redis server installed and running locally
- Code must follow `pycodestyle` (PEP8) style (version 2.5)
- All Python files must:
  - Have the first line `#!/usr/bin/env python3`
  - End with a new line
  - Contain module, class, and function docstrings
  - Use type annotations

---

## Setup Instructions

Install Redis and dependencies:

```bash
sudo apt-get update
sudo apt-get install redis-server
sudo service redis-server start
python3 -m venv venv
source venv/bin/activate
pip install redis
