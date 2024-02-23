import asyncio
import hashlib
import random
import string
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

# Setup synchronous MongoDB client with pymongo
client = MongoClient("mongodb://localhost:27017/")
db = client["test-database"]
collection = db["test-collection"]

def generate_random_string(length=10):
    """Generate a random string of fixed length."""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def create_code_hash():
    """Create a random code hash."""
    random_string = generate_random_string()
    hash_object = hashlib.sha256(random_string.encode())
    code_hash = hash_object.hexdigest()
    return code_hash

def insert_request(request_body):
    """Insert a request into the MongoDB collection."""
    try:
        collection.insert_one(request_body)
    except Exception as e:
        print(f"Error occurred: {e}")

async def make_request():
    """Create and insert a request asynchronously."""
    code_hash = create_code_hash()
    key = generate_random_string()
    row = str(random.randint(1, 10))
    col = str(random.randint(1, 10))

    request_body = {
        "code_hash": code_hash,
        "phase": "1",
        "start_key": "RAP0",
        "site": "test.com",
        "key": key,
        "func_name": "n",
        "js": "https://inte.searchnode.io/kasa/searchnode.min.js?1701252262",
        "row": row,
        "col": col,
        "func": "function n(r){if(e[r])return e[r].exports;var i=e[r]={i:r,l:!1,exports:{}};return t[r].call(i.exports,i,i.exports,n),i.l=!0,i.exports"
    }

    # Use a thread pool to execute the synchronous MongoDB operation
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, insert_request, request_body)

async def main(rate_per_second, duration_seconds):
    interval = 1.0 / rate_per_second
    total_requests = rate_per_second * duration_seconds

    tasks = [make_request() for _ in range(total_requests)]
    for i in range(0, total_requests, rate_per_second):
        batch = tasks[i:i + rate_per_second]
        await asyncio.gather(*batch)
        await asyncio.sleep(interval)

# clear the collection
# collection.delete_many({})

# Send 100 requests per second for 10 seconds
# rate_per_second = 1000
# duration_seconds = 10
# asyncio.run(main(rate_per_second, duration_seconds))

# Count the number of documents in the collection
count = collection.count({})
print(f"Total requests inserted: {count}")



