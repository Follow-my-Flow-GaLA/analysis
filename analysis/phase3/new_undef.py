from pymongo import MongoClient
import csv

client = MongoClient("mongodb://localhost:27017/")
phase1_db = client["phase1"]
phase3_db = client["phase3"]

# phase_dict = {site: {codehash: {key: [row_col (array), js_name, func_name]}}}
def get_phase_info(site, phase_db):
    phase_info = phase_db["phase_info"].find_one({
        "_id": site
    })
    return phase_info


def process_site(site):
    try: 
        phase3_info = get_phase_info(site, phase3_db)
        if phase3_info is None:
            return 
        phase1_info = get_phase_info(site, phase1_db)
        if phase1_info is None:
            return
    except Exception as e:
        print(f"Error: Failed to get phase info for {site}. Error: {e}")
        return
    new_undef_dict = find_new_undef(phase1_info, phase3_info)
    post_new_undef(site, new_undef_dict)
    

# Function to find new undefined values in phase3 that are not in phase1
def find_new_undef(phase1_info, phase3_info):
    new_undef_dict = {}
    for codehash, phase3_codehash_dict in phase3_info["code_hash_dict"].items():
        # add new codehash with all contents in it
        if codehash not in phase1_info["code_hash_dict"]:
            new_undef_dict[codehash] = phase3_codehash_dict
            continue
        phase1_codehash_dict = phase1_info["code_hash_dict"][codehash]
        for key, value in phase3_codehash_dict.items():
            # TODO: check row_col, js_name, func_name?
            if key in phase1_codehash_dict:
                continue
            # add key value to new_undef_dict
            if codehash not in new_undef_dict:
                new_undef_dict[codehash] = {}
            new_undef_dict[codehash][key] = value
    return new_undef_dict


# post new_undef_dict to db
def post_new_undef(site, new_undef_dict):
    try:
        phase3_db["new_undef"].update_one(
            {"_id": site},
            {"$set": {
                "new_undef": new_undef_dict
            }},
            upsert=True
        )
    except Exception as e:
        print(f"Error: Failed to post new_undef_dict for {site}. Error: {e}")
        return


WEB_LIST_PATH = "/media/datak/inactive/sanchecker/src/tranco_LJ494.csv"
NUM_OF_WEB_TO_CRAWL = -1
if __name__ == "__main__":
    counter = 0
    # extract domains from csv
    with open(WEB_LIST_PATH, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                site = row[1].replace('.', '_')
                counter += 1
                # process site
                process_site(site)
            if NUM_OF_WEB_TO_CRAWL > 0 and counter >= NUM_OF_WEB_TO_CRAWL:
                break
            if counter % 100000 == 0:
                print(f"Processed {counter} sites.")
