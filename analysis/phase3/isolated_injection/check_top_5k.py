from pymongo import MongoClient
import csv
import json

client = MongoClient("mongodb://localhost:27017/")
phase3_db = client["phase3"]
data_to_change_collection = phase3_db["data_to_change"]
result_dict = {}

with open("/media/datak/inactive/sanchecker/src/tranco_LJ494.csv", newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row:
            if int(row[0]) > 10:
                break
            site = row[1].replace(".", "_")
            site_info = data_to_change_collection.find_one({"_id": site})
            if site_info:
                data_to_change = site_info.get("data_to_change", [])
                result_dict[site] = data_to_change

with open("top_5k_data_to_change.json", "w") as f:
    json.dump(result_dict, f)