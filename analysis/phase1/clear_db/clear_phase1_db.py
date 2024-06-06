import pymongo 

db = pymongo.MongoClient("mongodb://localhost:27017/")["phase1"]

print('Type "Confirm_Delete_Phase1" to confirm the deletion')
confirm_msg = input('Type here: ')
if confirm_msg == "Confirm_Delete_Phase1":
    db["undef_prop_dataset"].delete_many({})
    db["phase_info"].delete_many({})
    db["code_hash_dataset"].delete_many({})
    print('All data from phase1 has been deleted')
else:
    print("Deletion not confirmed")