from pymongo import MongoClient
import csv
import time

client = MongoClient("mongodb://localhost:27017/")
phase1_db = client["phase1"]
phase_info_collection = phase1_db["phase_info"]
js_name_set = set()

start_time = time.time()

# extract domains from csv
file_path = "/media/datak/inactive/sanchecker/src/tranco_LJ494.csv"
with open(file_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row:
            if int(row[0]) % 100000 == 0:
                print(row[0], "Time elapsed: ", time.time() - start_time)
            site = row[1].replace(".", "_")
            site_info = phase_info_collection.find_one({"_id": site})
            if site_info:
                code_hash_dict = site_info.get("code_hash_dict", {})
                for code_hash, code_hash_obj in code_hash_dict.items():
                    for key in code_hash_obj:
                        js_name = code_hash_obj[key][1]
                        # Convert . and $ back
                        js_name = js_name.replace("\\2E", ".").replace("\\24", "$")
                        js_name_set.add(js_name)

# Write to file line by line
with open("js_name_2.txt", "w") as f:
    for js_name in js_name_set:
        f.write(js_name + "\n")

# Print the total number of js names
print("Total JS names: ", len(js_name_set))
