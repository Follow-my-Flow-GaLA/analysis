import pymongo 

db = pymongo.MongoClient("mongodb://localhost:27017/")["phase3"]

print('Type "Confirm_Delete_Phase3" to confirm the deletion')
confirm_msg = input('Type here: ')
if confirm_msg == "Confirm_Delete_Phase3":
    db["data_to_change"].delete_many({})
    print('All data from phase3 has been deleted')
else:
    print("Deletion not confirmed")