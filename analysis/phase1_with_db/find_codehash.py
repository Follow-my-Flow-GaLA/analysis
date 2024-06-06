from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["phase1"]
phase_info_collection = db["phase_info"]
undef_prop_dataset_collection = db["undef_prop_dataset"]
code_hash_dataset_collection = db["code_hash_dataset"]
# 7627220075580804bbe167aef3f9d211d129ed1f33202959e0f2a70ea657d3f1
# 2601d9b514349a11075806621ba29afac6ed6442848d30444b1023d98646262a

# code_hash = "e5ca1998415563c2a6fff3472f0a9eaf17b68353375341461d10c6f40a0dd412"
# code_hash_obj = undef_prop_dataset_collection.find_one({"_id": code_hash})
# if (code_hash_obj):
#     print("Code hash exists")
#     print(len(code_hash_obj["key_dict"]))
#     print(code_hash_obj["key_dict"])
# else:
#     print("Code hash does not exist")
# hashed_func = code_hash_dataset_collection.find_one({"_id": code_hash})
# if (hashed_func):
#     print("Hashed func exists")
#     print(len(hashed_func["func"]))
#     print(hashed_func["func"])
# else:
#     print("Hashed func does not exist")

site = "mountvernon_org"
key = "ar"
js = "https://global.localizecdn.com/localize.js".replace(".", "\\2E").replace("$", "\\24")
# first, find if the key and js exist in phase info
phase_info_obj = phase_info_collection.find_one({"_id": site})
code_hash_dict = phase_info_obj["code_hash_dict"]
for code_hash in code_hash_dict:
    if key in code_hash_dict[code_hash]:
        if code_hash_dict[code_hash][key][1] == js:
            print("Key already exists in phase_info")
            print(code_hash)
            break
# second, find if the key exists in undef_prop_dataset
for code_hash in code_hash_dict:
    code_hash_obj = undef_prop_dataset_collection.find_one({"_id": code_hash})
    if key in code_hash_obj["key_dict"]:
        print("Key already exists in undef_prop_dataset")
        print(code_hash_obj)
        break
