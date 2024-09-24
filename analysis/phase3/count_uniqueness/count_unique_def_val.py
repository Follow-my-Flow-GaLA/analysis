from pymongo import MongoClient
import hashlib
from tqdm import tqdm

client = MongoClient('mongodb://localhost:27017/')
db = client['phase3']
print("Collections in the database:", db.list_collection_names())

collection = db['cookie_url_exploit']

hashed_def_val_set = set()

count_multiple_payload = 0

# Get the total number of documents for the progress bar
total_docs = collection.count_documents({})
print("Number of Total Documents: ", total_docs)

cursor = collection.find({})
for document in tqdm(cursor, total=total_docs, desc="Processing documents"):
    data_list = document["cookie_url_exploit"]
    for data in data_list:
        # # skip dummy paylod
        # if data["payload"] == "~":
        #     continue
        # if isinstance(data["payload"], list):
        #     count_multiple_payload += 1
        # hash data
        hash_object = hashlib.sha256()
        hash_object.update(str(data).encode('utf-8'))
        hashed_string = hash_object.hexdigest()
        # add hashed value to set
        hashed_def_val_set.add(hashed_string)

print(count_multiple_payload)
print(len(hashed_def_val_set))
# data_to_change: 581278
# exploit: 1160
# cookie_url_exploit: 3279
