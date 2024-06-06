from pymongo import MongoClient

number_of_unique_data = 0
unique_data_to_change_dict = {}

client = MongoClient("mongodb://localhost:27017/")
phase1_db = client["phase1"]
phase3_db = client["phase3"]

def get_data_to_change(site):
    data_to_change = phase3_db["data_to_change"].find_one({
        "_id": site
    })
    return data_to_change

def get_phase1_info(site):
    phase_info = phase1_db["phase_info"].find_one({
        "_id": site
    })
    return phase_info

website_list = phase3_db["data_to_change"].distinct("_id")
for site in website_list:
    try:
        data_to_change = get_data_to_change(site)
        if data_to_change is None:
            continue
        phase1_info = get_phase1_info(site)
        if phase1_info is None:
            continue
    except Exception as e:
        # print(f"Error: Failed to get data to change for {site}. Error: {e}")
        continue
    
    # although there shouldn't be dummy data, we still filter them out 
    # then turn the data to change into a set
    data_to_change_set = set()
    for data in data_to_change["data_to_change"]:
        if data["payload"] != "~":
            # only save row_col and file_name
            row_col_list = data["row_col"]
            file_name = data["file_name"]
            for row_col in row_col_list:
                data_to_change_set.add(str((row_col, file_name)))
    
    for codehash, key_dict in phase1_info["code_hash_dict"].items():
        for key in key_dict:
            row_col_list = key_dict[key][0]
            file_name = key_dict[key][1]
            for row_col in row_col_list:
                if str((row_col, file_name)) in data_to_change_set:
                    if codehash not in unique_data_to_change_dict:
                        unique_data_to_change_dict[codehash] = set()
                    unique_data_to_change_dict[codehash].add(str((row_col, file_name)))

# count the number of unique data to change
for codehash in unique_data_to_change_dict:
    number_of_unique_data += len(unique_data_to_change_dict[codehash])
print(f"Number of unique data to change: {number_of_unique_data}")                    
    
    
    
    
    
    
    