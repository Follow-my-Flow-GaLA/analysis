from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["phase3"]
def_val_dataset_collection = db["def_val_dataset"]
phase_info_collection = db["phase_info"]
data_to_change_collection = db["data_to_change"]

print(data_to_change_collection.find_one({
    "_id": "yuanshen_com"
}))