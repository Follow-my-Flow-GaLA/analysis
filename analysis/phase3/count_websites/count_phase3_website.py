from pymongo import MongoClient
import csv
import time
client = MongoClient("mongodb://localhost:27017/")
phase3_db = client["phase3"]
data_to_change_collection = phase3_db["data_to_change"]

data_to_change_web_list = []
non_dummy_web_list = []
start_time = time.time()

'''
# count all websites in data to change 
'''
# extract domains from csv
all_web_file_path = "/media/datak/inactive/sanchecker/src/tranco_LJ494.csv"
with open(all_web_file_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row:
            if int(row[0]) % 100000 == 0:
                print(row[0], "Time elapsed: ", time.time() - start_time)
            site = row[1].replace(".", "_")
            site_info = data_to_change_collection.find_one({"_id": site})
            if site_info:
                data_to_change_web_list.append(row[1])
                # check if the website has non-dummy value
                data_to_change = site_info.get("data_to_change", [])
                for data in data_to_change:
                    if data["payload"] != "~":
                        non_dummy_web_list.append(row[1])
                        break
        
# Write to file line by line
data_to_change_count = 1
with open("phase3_data_to_change_website_list.txt", "w") as f:
    for website in data_to_change_web_list:
        f.write(str(data_to_change_count) + "," + website + "\n")
        data_to_change_count += 1
        
# Print the total number of websites
print("Total websites: ", data_to_change_count-1)

non_dummy_count = 1
with open("phase3_data_to_change_non_dummy_website_list.txt", "w") as f:
    for website in non_dummy_web_list:
        f.write(str(non_dummy_count) + "," + website + "\n")
        non_dummy_count += 1
        
print("Total non-dummy websites: ", non_dummy_count-1)
