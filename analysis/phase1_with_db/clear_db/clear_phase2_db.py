import pymongo 

db = pymongo.MongoClient("mongodb://localhost:27017/")["phase2"]

print('Type "Confirm_Delete_Phase2" to confirm the deletion')
confirm_msg = input('Type here: ')
if confirm_msg == "Confirm_Delete_Phase2":
    db["phase_info"].delete_many({})
    db["def_val_dataset"].delete_many({})
    print('All data from phase2 has been deleted')
else:
    print("Deletion not confirmed")