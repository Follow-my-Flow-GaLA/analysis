from pymongo import MongoClient
import csv

number_of_unique_def_val = 0
codehash_set = set()

client = MongoClient("mongodb://localhost:27017/")
phase2_db = client["phase2"]

# failed_flow[code_hash_dict] = {codehash: {key: [value, row_col(str), sink_type]]}}
def get_failed_flow(site):
    failed_flow = phase2_db["failed_flow"].find_one({
        "_id": site
    })
    return failed_flow

# failed_val_dataset[key_value_dict] = {key: {"value": value, "sink_type": sink_type, "site": site}}
def get_failed_val_dataset(codehash):
    failed_val_dataset = phase2_db["failed_val_dataset"].find_one({
        "_id": codehash
    })
    return failed_val_dataset

def process_site(site):
    global codehash_set
    try: 
        failed_flow = get_failed_flow(site)
        if failed_flow is None:
            return False
    except Exception as e:
        # print(f"Error: Failed to get phase info for {site}. Error: {e}")
        return False
    for codehash in failed_flow["code_hash_dict"].keys():
        if codehash not in codehash_set:
            process_codehash(codehash)
            codehash_set.add(codehash)
    return True


def process_codehash(codehash):
    global number_of_unique_def_val
    try:
        failed_val_dataset = get_failed_val_dataset(codehash)
        if failed_val_dataset is None:
            return
    except Exception as e:
        # print(f"Error: Failed to get undef prop dataset for {codehash}. Error: {e}")
        return
    number_of_unique_def_val += len(failed_val_dataset["key_value_dict"])
    

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
                # process site
                if process_site(site):
                    counter += 1
            if NUM_OF_WEB_TO_CRAWL > 0 and counter >= NUM_OF_WEB_TO_CRAWL:
                break
            if counter % 100000 == 0:
                print(f"Processed {counter} sites, {number_of_unique_def_val}.")
    print(f"Total number of unique defined values (failed flow): {number_of_unique_def_val}.")
    print(f"Total number of unique codehash: {len(codehash_set)}.")