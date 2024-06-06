import hashlib

a = "\xa9 \x0a"
sha256_hash = hashlib.sha256()
sha256_hash.update(a.encode('ascii'))
hash_func = sha256_hash.hexdigest()
print(hash_func)

