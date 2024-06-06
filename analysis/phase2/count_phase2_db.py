from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
phase2_db = client["phase2"]
def_val_dataset_collection = phase2_db["def_val_dataset"]

# get all code_hash in def_val_dataset
code_hash_list = def_val_dataset_collection.distinct("_id")
print("Total code_hash in def_val_dataset: ", len(code_hash_list))

sink_type_dict = {}
# loop through all code_hash
for code_hash in code_hash_list:
    def_val_obj = def_val_dataset_collection.find_one({"_id": code_hash})
    if not def_val_obj:
        print("Error: def_val_dataset for code_hash " + code_hash + " not found")
        continue
    key_value_dict = def_val_obj["key_value_dict"]
    for key in key_value_dict:
        sink_type = key_value_dict[key]["sink_type"]
        if sink_type not in sink_type_dict:
            sink_type_dict[sink_type] = 1
        else:
            sink_type_dict[sink_type] += 1
print(sink_type_dict)
