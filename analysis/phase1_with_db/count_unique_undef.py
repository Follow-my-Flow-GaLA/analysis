from pymongo import MongoClient
import csv

number_of_unique_undef_with_diff_row_col = 0
number_of_unique_undef_key = 0
codehash_set = set()

client = MongoClient("mongodb://localhost:27017/")
phase1_db = client["phase1"]

# phase_info[code_hash_dict] = {codehash: {key: [row_col (array), js_name, func_name]}}
def get_phase_info(site):
    phase_info = phase1_db["phase_info"].find_one({
        "_id": site
    })
    return phase_info

# undef_prop_dataset[key_dict] = {key: row_col(array)}
def get_undef_prop_dataset(codehash):
    undef_prop_dataset = phase1_db["undef_prop_dataset"].find_one({
        "_id": codehash
    })
    return undef_prop_dataset

def process_site(site):
    global codehash_set
    try: 
        phase1_info = get_phase_info(site)
        if phase1_info is None:
            return 
    except Exception as e:
        # print(f"Error: Failed to get phase info for {site}. Error: {e}")
        return
    for codehash in phase1_info["code_hash_dict"].keys():
        if codehash not in codehash_set:
            process_codehash(codehash)
            codehash_set.add(codehash)


def process_codehash(codehash):
    global number_of_unique_undef_with_diff_row_col, number_of_unique_undef_key
    try:
        undef_prop_dataset = get_undef_prop_dataset(codehash)
        if undef_prop_dataset is None:
            return
    except Exception as e:
        # print(f"Error: Failed to get undef prop dataset for {codehash}. Error: {e}")
        return
    number_of_unique_undef_key += len(undef_prop_dataset["key_dict"])
    # for keys having the same row_col, they are considered the same
    row_col_set = set()
    for key, row_col_list in undef_prop_dataset["key_dict"].items():    
        for row_col in row_col_list:
            row_col_set.add(row_col)        
    number_of_unique_undef_with_diff_row_col += len(row_col_set)
    

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
                print(f"Processed {counter} sites, {number_of_unique_undef_with_diff_row_col}, {number_of_unique_undef_key}.")
                break
    print(f"Total number of unique undef key: {number_of_unique_undef_key}.")
    print(f"Total number of unique undef with different row_col: {number_of_unique_undef_with_diff_row_col}.")
    print(f"Total number of unique codehash: {len(codehash_set)}.")