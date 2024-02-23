import asyncio
import aiohttp
import hashlib
import random
import string

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

async def make_request(session, url):
    # Create random request body
    # required_fields = ['phase', 'start_key', 'site', 'key', 'func_name', 'js', 'row', 'col', 'func']
    
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
        
    try:
        # Send request without waiting for the response
        asyncio.create_task(session.post(url, json=request_body))
        print("Request sent")
    except Exception as e:
        print(f"Error occurred: {e}")

async def main(url, rate_per_second, duration_seconds):
    async with aiohttp.ClientSession() as session:
        interval = 1.0 / rate_per_second
        total_requests = rate_per_second * duration_seconds

        for _ in range(total_requests):
            asyncio.create_task(make_request(session, url))
            await asyncio.sleep(interval)

# URL to your target endpoint
url = 'http://127.0.0.1:5000/api/phase1/undefined_value'

# Send 100 requests per second for 10 seconds
asyncio.run(main(url, 20, 100))

