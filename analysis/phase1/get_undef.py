from pymongo import MongoClient
import csv
import time

client = MongoClient("mongodb://localhost:27017/")
db = client["phase1"]

WEB_LIST_PATH = "/media/datak/inactive/sanchecker/src/tranco_LJ494.csv"
NUM_OF_WEB_TO_CRAWL = 5000

def get_web_list(file_path=WEB_LIST_PATH, limit=NUM_OF_WEB_TO_CRAWL):
    web_list = []
    counter = 0
    # extract domains from csv
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                web_list.append(row[1])
                counter += 1
            if counter >= limit:
                break
    return web_list

def get_phase_info(site):
    phase_info = db["phase_info"].find_one({
        "_id": site
    })
    return phase_info

start_time = time.time()

web_list = get_web_list()
print(web_list)
print("get web_list: ", time.time() - start_time)
'''
undef_dict = {
    "site_url1": {
        "js_url1": {
            "undef_prop_1": {
                "row1": ["col1", "col2"],
                "row2": ...
            }
            "undef_prop_2": ...
        }
    },
    "site_url2": ...
}
'''
undef_dict = {}
for web in web_list:
    site = web.replace(".", "_")
    phase_info = get_phase_info(site)
    if phase_info is None:
        print(f"Phase info for {web} is not found.")
        continue
    site_dict = {}
    for codehash, codehash_info in phase_info["code_hash_dict"].items():
        for undef_prop, undef_prop_info in codehash_info.items():
            undef_prop = undef_prop.replace("\\2E", ".").replace("\\24", "$")
            js_url = undef_prop_info[1].replace("\\2E", ".").replace("\\24", "$")
            if site_dict.get(js_url) is None:
                site_dict[js_url] = {}
            if site_dict[js_url].get(undef_prop) is None:
                site_dict[js_url][undef_prop] = {}
            
            row_col_list = undef_prop_info[0]
            for row_col in row_col_list:
                row = row_col.split(", ")[0]
                col = row_col.split(", ")[1]
                if site_dict[js_url][undef_prop].get(row) is None:
                    site_dict[js_url][undef_prop][row] = []
                # add col without duplicates
                if col not in site_dict[js_url][undef_prop][row]:
                    site_dict[js_url][undef_prop][row].append(col)
                
    undef_dict[site] = site_dict

print("get undef_dict: ", time.time() - start_time)
print("output to json...")
import json
with open('undef_dict.json', 'w') as f:
    json.dump(undef_dict, f)
print("Done: ", time.time() - start_time)