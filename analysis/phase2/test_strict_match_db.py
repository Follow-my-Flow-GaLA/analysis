from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
phase1_db = client["phase1"]
phase2_db = client["phase2"]
phase3_db = client["phase3"]

db_post_error_count = 0

# load website list from db
def load_website_list():
    try:
        return phase1_db["phase_info"].distinct("_id")
    except Exception as e:
        print("Error when loading website list: " + str(e))
    return []

# get phase1 info for a website
def get_phase1_info(website):
    try:
        return phase1_db["phase_info"].find_one({"_id": website})
    except Exception as e:
        print("Error when loading phase1 info for website " + website + ": " + str(e))
    return []

# get def_val_dataset for a code_hash
def get_def_value_dataset(code_hash):
    try:
        def_value_dict = phase2_db["def_val_dataset"].find_one({"_id": code_hash})
        if not def_value_dict:
            print("Error: def_val_dataset for code_hash " + code_hash + " not found")
        else:
            return def_value_dict
    except Exception as e:
        print("Error: Failed to load def_val_dataset for code_hash " + code_hash)
    return {}

# post data to change to db
def post_data_to_change_to_db(payload):
    # add site to data_to_change only if it does not exist
    phase3_db["data_to_change"].update_one(
        {"_id": payload["site"]}, 
        {"$setOnInsert": {
            "data_to_change": []
        }},
        upsert=True
    )
    # append data to change
    phase3_db["data_to_change"].update_one(
        {"_id": payload["site"]},
        {"$push": {
            "data_to_change": {
                "var_name": payload["var_name"],
                "payload": payload["payload"],
                "row_col": payload["row_col"],
                "file_name": payload["file_name"]
            }
        }}
    )

# this is strict match with dummy value (i.e. if the value is not matched, then it has dummy value "~")
def strict_match_with_dummy_value(website_list):
    for website in website_list:
        dummy_value_count = 0
        not_dummy_count = 0
        # get phase 1 info
        phase1_info = get_phase1_info(website)
        # get all code_hash in phase1_info
        print(phase1_info)
        for code_hash, undef_prop_dict in phase1_info["code_hash_dict"].items():
            # get def_val_dataset for this code_hash
            def_value_dataset = get_def_value_dataset(code_hash)
            if not def_value_dataset:
                continue
            def_value_dict = get_def_value_dataset(code_hash)["key_value_dict"]
            # match undef_prop_dict and def_value_dict
            for undef_prop_key in undef_prop_dict.keys():
                payload = {
                    "phase": "3",
                    "site": website,
                    "var_name": undef_prop_key,
                    "row_col": undef_prop_dict[undef_prop_key][0],
                    "file_name": undef_prop_dict[undef_prop_key][1],
                }
                if undef_prop_key in def_value_dict: # matched
                    payload["payload"] = def_value_dict[undef_prop_key]["value"]
                    not_dummy_count += 1
                else: # not matched, use dummy value "~"
                    payload["payload"] = "~"
                    dummy_value_count += 1
                # post to db
                post_data_to_change_to_db(payload) 
        print("Dummy value count: " + str(dummy_value_count))
        print("Not dummy value count: " + str(not_dummy_count))

if __name__ == "__main__":
    website_list = ['mountvernon_org']
    strict_match_with_dummy_value(website_list)